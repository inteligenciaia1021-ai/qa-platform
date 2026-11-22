from qa_platform.knowledge.fingerprint import gerar_fingerprint


def test_erros_parecidos_geram_mesmo_fingerprint():
    a = gerar_fingerprint("backend", "Erro na linha 42 do arquivo /home/ana/app.py")
    b = gerar_fingerprint("backend", "Erro na linha 97 do arquivo /srv/app/main.py")
    assert a == b


def test_modulos_diferentes_geram_fingerprints_diferentes():
    a = gerar_fingerprint("backend", "timeout")
    b = gerar_fingerprint("frontend", "timeout")
    assert a != b