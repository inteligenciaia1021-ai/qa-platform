from qa_platform.modules.frontend import Frontend

PAGINA_OK = (
    "<!doctype html><html><head><title>Ok</title></head>"
    "<body><h1>Oi</h1></body></html>"
)


def _site(pasta, html):
    (pasta / "index.html").write_text(html, encoding="utf-8")
    return str(pasta)


def _mensagens(falhas):
    return [f.mensagem for f in falhas]


def test_pagina_limpa_nao_gera_falhas(tmp_path):
    assert Frontend().rodar(_site(tmp_path, PAGINA_OK)) == []


def test_detecta_erro_de_javascript(tmp_path):
    html = PAGINA_OK.replace("</body>", '<script>throw new Error("quebrou")</script></body>')
    mensagens = _mensagens(Frontend().rodar(_site(tmp_path, html)))
    assert any("Erro de JavaScript" in m and "quebrou" in m for m in mensagens)


def test_detecta_recurso_nao_encontrado(tmp_path):
    html = PAGINA_OK.replace("</body>", '<img src="sumiu.png" alt="x"></body>')
    mensagens = _mensagens(Frontend().rodar(_site(tmp_path, html)))
    assert any(m.startswith("Recurso não encontrado") for m in mensagens)


def test_detecta_pagina_sem_titulo(tmp_path):
    html = "<!doctype html><html><head></head><body><h1>Oi</h1></body></html>"
    mensagens = _mensagens(Frontend().rodar(_site(tmp_path, html)))
    assert "Página sem título" in mensagens


def test_detecta_imagem_sem_alt(tmp_path):
    gif = "data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7"
    html = PAGINA_OK.replace("</body>", f'<img src="{gif}"></body>')
    mensagens = _mensagens(Frontend().rodar(_site(tmp_path, html)))
    assert any(m.startswith("Imagem sem texto alternativo") for m in mensagens)


def test_endereco_inexistente_e_reportado():
    falhas = Frontend().rodar("http://127.0.0.1:1/")
    assert len(falhas) == 1
    assert falhas[0].mensagem.startswith("Página não abriu")