from qa_platform.modules.code_quality import CodeQuality


def test_detecta_import_nao_usado(tmp_path):
    (tmp_path / "ruim.py").write_text("import os\n")
    falhas = CodeQuality().rodar(str(tmp_path))
    assert len(falhas) == 1
    assert falhas[0].mensagem.startswith("F401")
    assert falhas[0].linha == 1


def test_codigo_limpo_nao_gera_falhas(tmp_path):
    (tmp_path / "ok.py").write_text("x = 1\n")
    assert CodeQuality().rodar(str(tmp_path)) == []