import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import pytest

from qa_platform.modules.deploy import Deploy, _mensagem_certificado

DOCKERFILE_BOM = (
    "FROM python:3.12-slim\n"
    "COPY . /app\n"
    "USER app\n"
    'CMD ["python", "app.py"]\n'
)


def _analisar(pasta, conteudo):
    (pasta / "Dockerfile").write_text(conteudo, encoding="utf-8")
    return Deploy().rodar(str(pasta))


def test_dockerfile_bom_nao_gera_falhas(tmp_path):
    assert _analisar(tmp_path, DOCKERFILE_BOM) == []


def test_imagem_latest_e_reportada(tmp_path):
    falhas = _analisar(tmp_path, "FROM python:latest\nUSER app\n")
    assert len(falhas) == 1
    assert falhas[0].mensagem.startswith("Imagem base sem versão fixa")


def test_imagem_sem_etiqueta_e_reportada(tmp_path):
    falhas = _analisar(tmp_path, "FROM python\nUSER app\n")
    assert len(falhas) == 1
    assert falhas[0].mensagem.startswith("Imagem base sem versão fixa")


def test_container_como_root_e_reportado(tmp_path):
    falhas = _analisar(tmp_path, "FROM python:3.12-slim\nCOPY . /app\n")
    assert len(falhas) == 1
    assert falhas[0].mensagem.startswith("Container roda como administrador")


def test_multi_stage_so_olha_o_ultimo_estagio(tmp_path):
    conteudo = "FROM python:3.12 AS build\nRUN pip install x\nFROM build\nUSER app\n"
    assert _analisar(tmp_path, conteudo) == []


def test_add_no_lugar_de_copy_e_reportado(tmp_path):
    falhas = _analisar(tmp_path, "FROM python:3.12-slim\nADD . /app\nUSER app\n")
    assert len(falhas) == 1
    assert falhas[0].mensagem.startswith("ADD usado")


def test_segredo_e_reportado_sem_mostrar_o_valor(tmp_path):
    conteudo = "FROM python:3.12-slim\nENV API_TOKEN=abc123\nUSER app\n"
    falhas = _analisar(tmp_path, conteudo)
    assert len(falhas) == 1
    assert falhas[0].mensagem.startswith("Segredo escrito no Dockerfile")
    assert "abc123" not in falhas[0].mensagem


def test_curl_direto_no_shell_e_reportado(tmp_path):
    conteudo = (
        "FROM python:3.12-slim\n"
        "RUN curl -fsSL https://exemplo.com/install.sh | sh\n"
        "USER app\n"
    )
    falhas = _analisar(tmp_path, conteudo)
    assert len(falhas) == 1
    assert falhas[0].mensagem.startswith("Download executado direto")


def test_pasta_sem_dockerfile_nao_vira_tudo_limpo(tmp_path):
    falhas = Deploy().rodar(str(tmp_path))
    assert len(falhas) == 1
    assert falhas[0].mensagem.startswith("Nada para verificar")


def test_aviso_de_certificado():
    assert _mensagem_certificado(90) is None
    assert _mensagem_certificado(10).startswith("Certificado perto de vencer")
    assert _mensagem_certificado(-1).startswith("Certificado inválido")


class _Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/lento":
            time.sleep(0.5)
        codigo = {"/erro": 500, "/sumiu": 404}.get(self.path, 200)
        self.send_response(codigo)
        self.send_header("Content-Length", "2")
        self.end_headers()
        self.wfile.write(b"ok")

    def log_message(self, *args):
        pass


@pytest.fixture
def servidor():
    srv = ThreadingHTTPServer(("127.0.0.1", 0), _Handler)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    yield f"http://127.0.0.1:{srv.server_address[1]}"
    srv.shutdown()
    srv.server_close()


def test_servidor_saudavel_nao_gera_falhas(servidor):
    assert Deploy().rodar(f"{servidor}/ok") == []


def test_erro_500_e_reportado(servidor):
    falhas = Deploy().rodar(f"{servidor}/erro")
    assert len(falhas) == 1
    assert "HTTP 500" in falhas[0].mensagem


def test_erro_404_e_reportado(servidor):
    falhas = Deploy().rodar(f"{servidor}/sumiu")
    assert len(falhas) == 1
    assert "HTTP 404" in falhas[0].mensagem


def test_resposta_lenta_e_reportada(servidor):
    falhas = Deploy(limite_lento=0.2).rodar(f"{servidor}/lento")
    assert len(falhas) == 1
    assert falhas[0].mensagem.startswith("Resposta lenta")


def test_servidor_fora_do_ar_e_reportado():
    falhas = Deploy().rodar("http://127.0.0.1:1/")
    assert len(falhas) == 1
    assert falhas[0].mensagem.startswith("Servidor não respondeu")