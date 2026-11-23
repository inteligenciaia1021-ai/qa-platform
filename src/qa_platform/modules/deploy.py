import os
import re
import shlex
import socket
import ssl
import time
import urllib.error
import urllib.request
from pathlib import Path
from urllib.parse import urlparse

from qa_platform.modules.base import Falha

NOME = "deploy"
LIMITE_LENTO = 2.0
TIMEOUT = 10
DIAS_ALERTA_CERTIFICADO = 30
SEGUNDOS_POR_DIA = 86400

_IGNORAR = {".venv", "node_modules", ".git"}
_PALAVRAS_SEGREDO = (
    "PASSWORD", "PASSWD", "SECRET", "TOKEN", "API_KEY", "APIKEY", "PRIVATE_KEY",
)
_COMPACTADOS = (".tar", ".tar.gz", ".tgz", ".tar.xz", ".tar.bz2")
_CURL_SH = re.compile(r"\b(curl|wget)\b[^|;&]*\|\s*(sudo\s+)?(ba|z)?sh\b")


# ---------- verificação de um servidor no ar ----------


def _mensagem_certificado(dias: int) -> str | None:
    if dias < 0:
        return "Certificado inválido: vencido"
    if dias <= DIAS_ALERTA_CERTIFICADO:
        return f"Certificado perto de vencer: faltam {dias} dias"
    return None


def _dias_para_vencer(url: str) -> int | None:
    partes = urlparse(url)
    host = partes.hostname
    if not host:
        return None
    porta = partes.port or 443
    try:
        contexto = ssl.create_default_context()
        with socket.create_connection((host, porta), timeout=TIMEOUT) as sock, \
                contexto.wrap_socket(sock, server_hostname=host) as seguro:
            certificado = seguro.getpeercert()
        vence = ssl.cert_time_to_seconds(certificado["notAfter"])
    except (OSError, KeyError, ValueError):
        return None
    return int((vence - time.time()) // SEGUNDOS_POR_DIA)


def _verificar_url(url: str, limite: float) -> list[str]:
    inicio = time.perf_counter()
    try:
        # o endereço já foi validado: só http:// ou https://
        with urllib.request.urlopen(url, timeout=TIMEOUT) as resposta:  # nosec B310
            resposta.read(1024)
            status = resposta.status
    except urllib.error.HTTPError as erro:
        status = erro.code
    except urllib.error.URLError as erro:
        if isinstance(erro.reason, ssl.SSLCertVerificationError):
            return [f"Certificado inválido: {erro.reason.verify_message}"]
        return [f"Servidor não respondeu: {erro.reason}"]
    except OSError as erro:
        return [f"Servidor não respondeu: {erro}"]
    duracao = time.perf_counter() - inicio

    mensagens = []
    if status >= 400:
        mensagens.append(f"Servidor respondeu com erro (HTTP {status})")
    if duracao > limite:
        mensagens.append(f"Resposta lenta: {duracao:.1f} s (limite {limite:g} s)")
    if url.lower().startswith("https://"):
        dias = _dias_para_vencer(url)
        aviso = _mensagem_certificado(dias) if dias is not None else None
        if aviso:
            mensagens.append(aviso)
    return mensagens


# ---------- análise de Dockerfile ----------


def _separar(numero: int, texto: str) -> tuple[int, str, str]:
    partes = texto.strip().split(None, 1)
    return numero, partes[0].upper(), partes[1] if len(partes) > 1 else ""


def _instrucoes(texto: str) -> list[tuple[int, str, str]]:
    """Junta linhas continuadas com \\ e devolve (linha, instrução, argumentos)."""
    resultado = []
    atual = ""
    inicio = 0
    for numero, linha in enumerate(texto.splitlines(), start=1):
        limpa = linha.strip()
        if not limpa or limpa.startswith("#"):
            continue
        if not atual:
            inicio = numero
        continuada = limpa.endswith("\\")
        atual += (limpa[:-1].rstrip() if continuada else limpa) + " "
        if continuada:
            continue
        resultado.append(_separar(inicio, atual))
        atual = ""
    if atual:
        resultado.append(_separar(inicio, atual))
    return resultado


def _tag(imagem: str) -> str | None:
    if "@" in imagem:
        return "digest"
    nome = imagem.rsplit("/", 1)[-1]
    return nome.split(":", 1)[1] if ":" in nome else None


def _checar_from(numero: int, args: str, estagios: set[str]) -> list[tuple[int, str]]:
    tokens = [t for t in args.split() if not t.startswith("--")]
    if not tokens:
        return []
    imagem = tokens[0]
    achados = []
    ignorar = imagem.lower() in estagios or imagem.lower() == "scratch" or "$" in imagem
    if not ignorar and _tag(imagem) in (None, "latest"):
        achados.append((numero, f"Imagem base sem versão fixa: {imagem}"))
    if len(tokens) >= 3 and tokens[1].upper() == "AS":
        estagios.add(tokens[2].lower())
    return achados


def _checar_add(numero: int, args: str) -> list[tuple[int, str]]:
    fontes = [t for t in args.split() if not t.startswith("--")][:-1]
    if fontes and not any(f.lower().endswith(_COMPACTADOS) for f in fontes):
        return [(numero, "ADD usado onde COPY basta")]
    return []


def _checar_segredos(numero: int, nome: str, args: str) -> list[tuple[int, str]]:
    if nome not in ("ENV", "ARG"):
        return []
    try:
        partes = shlex.split(args)
    except ValueError:
        partes = args.split()
    pares = []
    if partes and "=" in partes[0]:
        pares = [p.split("=", 1) for p in partes if "=" in p]
    elif nome == "ENV" and len(partes) >= 2:
        pares = [[partes[0], " ".join(partes[1:])]]
    achados = []
    for chave, valor in pares:
        suspeita = any(p in chave.upper() for p in _PALAVRAS_SEGREDO)
        if suspeita and valor and not valor.startswith("$"):
            # só o nome da variável: o valor nunca vai para o relatório
            achados.append((numero, f"Segredo escrito no Dockerfile: variável {chave}"))
    return achados


def _checar_usuario(instrucoes: list[tuple[int, str, str]]) -> list[tuple[int, str]]:
    inicio = None
    usuario = None
    for numero, nome, args in instrucoes:
        if nome == "FROM":
            inicio, usuario = numero, None
        elif nome == "USER":
            usuario = args.split(":")[0].strip()
    if inicio is None:
        return []
    if usuario is None or usuario in ("root", "0"):
        return [(inicio, "Container roda como administrador (root)")]
    return []


def _analisar_dockerfile(caminho: Path) -> list[Falha]:
    texto = caminho.read_text(encoding="utf-8", errors="replace")
    instrucoes = _instrucoes(texto)
    achados: list[tuple[int, str]] = []
    estagios: set[str] = set()
    for numero, nome, args in instrucoes:
        if nome == "FROM":
            achados += _checar_from(numero, args, estagios)
        elif nome == "ADD":
            achados += _checar_add(numero, args)
        elif nome == "RUN" and _CURL_SH.search(args):
            achados.append((numero, "Download executado direto no shell (curl | sh)"))
        achados += _checar_segredos(numero, nome, args)
    achados += _checar_usuario(instrucoes)
    return [Falha(NOME, msg, str(caminho), linha) for linha, msg in achados]


def _achar_dockerfiles(pasta: Path) -> list[Path]:
    achados = []
    for raiz, subpastas, arquivos in os.walk(pasta):
        subpastas[:] = [p for p in subpastas if p not in _IGNORAR]
        for nome in arquivos:
            if nome == "Dockerfile" or nome.startswith("Dockerfile.") or nome.endswith(".Dockerfile"):
                achados.append(Path(raiz) / nome)
    return sorted(achados)


class Deploy:
    nome = NOME

    def __init__(self, limite_lento: float = LIMITE_LENTO):
        self.limite_lento = limite_lento

    def rodar(self, caminho: str) -> list[Falha]:
        if caminho.lower().startswith(("http://", "https://")):
            mensagens = _verificar_url(caminho, self.limite_lento)
            return [Falha(NOME, m, caminho) for m in mensagens]
        alvo = Path(caminho)
        if alvo.is_file():
            return _analisar_dockerfile(alvo)
        if alvo.is_dir():
            arquivos = _achar_dockerfiles(alvo)
            if not arquivos:
                mensagem = "Nada para verificar: nenhum Dockerfile encontrado"
                return [Falha(NOME, mensagem, caminho)]
            return [f for a in arquivos for f in _analisar_dockerfile(a)]
        mensagem = "Alvo não encontrado: não é um endereço nem um arquivo ou pasta existente"
        return [Falha(NOME, mensagem, caminho)]