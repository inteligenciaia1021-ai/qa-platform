import functools
import threading
from contextlib import contextmanager
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from qa_platform.modules.base import Falha

try:
    from playwright.sync_api import Error as PlaywrightError
    from playwright.sync_api import sync_playwright
except ImportError:  # Playwright ainda não instalado
    PlaywrightError = Exception
    sync_playwright = None


class _Silencioso(SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


@contextmanager
def _servir(pasta: str):
    handler = functools.partial(_Silencioso, directory=pasta)
    servidor = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = threading.Thread(target=servidor.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{servidor.server_address[1]}/"
    finally:
        servidor.shutdown()
        servidor.server_close()


def _console(msg, anotar) -> None:
    # Erros de carregamento já são tratados em _resposta; evita duplicar.
    if msg.type == "error" and not msg.text.startswith("Failed to load resource"):
        anotar(f"Erro de JavaScript na página: {msg.text}")


def _resposta(resp, anotar) -> None:
    if resp.url.endswith("/favicon.ico"):
        return
    if resp.status == 404:
        anotar(f"Recurso não encontrado (HTTP 404): {resp.url}")
    elif resp.status >= 500:
        anotar(f"Erro do servidor (HTTP {resp.status}): {resp.url}")
    elif resp.status >= 400:
        anotar(f"Resposta com erro (HTTP {resp.status}): {resp.url}")


def _rede(req, anotar) -> None:
    if not req.url.endswith("/favicon.ico"):
        anotar(f"Falha de rede ao carregar: {req.url}")


def _sem_duplicatas(mensagens: list[str]) -> list[str]:
    # Se um endereço já tem outro alerta (ex.: HTTP 404), a "falha de rede"
    # do mesmo endereço é a mesma causa contada duas vezes.
    prefixo = "Falha de rede ao carregar: "
    resultado = []
    for texto in mensagens:
        if texto.startswith(prefixo):
            endereco = texto[len(prefixo):]
            if any(endereco in outra for outra in mensagens if outra != texto):
                continue
        resultado.append(texto)
    return resultado


class Frontend:
    nome = "frontend"

    def rodar(self, caminho: str) -> list[Falha]:
        if Path(caminho).is_dir():
            with _servir(caminho) as url:
                return self._testar(url)
        return self._testar(caminho)

    def _testar(self, url: str) -> list[Falha]:
        if sync_playwright is None:
            raise RuntimeError(
                "Playwright não está instalado. Rode: pip install playwright "
                "e depois: playwright install chromium"
            )
        mensagens: list[str] = []

        def anotar(texto: str) -> None:
            if texto not in mensagens:
                mensagens.append(texto)

        with sync_playwright() as p:
            navegador = p.chromium.launch()
            try:
                pagina = navegador.new_page()
                pagina.on("pageerror", lambda erro: anotar(f"Erro de JavaScript na página: {erro}"))
                pagina.on("console", lambda msg: _console(msg, anotar))
                pagina.on("response", lambda resp: _resposta(resp, anotar))
                pagina.on("requestfailed", lambda req: _rede(req, anotar))
                try:
                    pagina.goto(url, wait_until="load")
                except PlaywrightError as erro:
                    motivo = str(erro).splitlines()[0]
                    return [Falha(self.nome, f"Página não abriu: {motivo}", url)]
                pagina.wait_for_timeout(500)
                if not pagina.title().strip():
                    anotar("Página sem título")
                sem_alt = pagina.eval_on_selector_all(
                    "img:not([alt])", "els => els.map(e => e.getAttribute('src') || '')"
                )
                for origem in sem_alt:
                    anotar(f"Imagem sem texto alternativo: {origem[:80]}")
            finally:
                navegador.close()
            return [Falha(self.nome, texto, url) for texto in _sem_duplicatas(mensagens)]