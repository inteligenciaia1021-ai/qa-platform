from qa_platform.modules.backend import Backend


def test_detecta_teste_que_falha(tmp_path):
    (tmp_path / "test_falha.py").write_text("def test_soma():\n    assert 1 + 1 == 3\n")
    falhas = Backend().rodar(str(tmp_path))
    assert len(falhas) == 1
    assert "assert" in falhas[0].mensagem
    assert "test_soma" in falhas[0].arquivo


def test_projeto_com_testes_passando_nao_gera_falhas(tmp_path):
    (tmp_path / "test_ok.py").write_text("def test_soma():\n    assert 1 + 1 == 2\n")
    assert Backend().rodar(str(tmp_path)) == []


def test_erro_de_importacao_mostra_o_motivo_real(tmp_path):
    (tmp_path / "test_import.py").write_text("import biblioteca_que_nao_existe_xyz\n")
    falhas = Backend().rodar(str(tmp_path))
    assert len(falhas) == 1
    assert "ModuleNotFoundError" in falhas[0].mensagem


def test_projeto_sem_testes_e_reportado(tmp_path):
    (tmp_path / "app.py").write_text("x = 1\n")
    falhas = Backend().rodar(str(tmp_path))
    assert len(falhas) == 1
    assert "Nenhum teste" in falhas[0].mensagem


def test_erro_de_importacao_nao_esconde_outras_falhas(tmp_path):
    (tmp_path / "test_import.py").write_text("import biblioteca_que_nao_existe_xyz\n")
    (tmp_path / "test_falha.py").write_text("def test_soma():\n    assert 1 + 1 == 3\n")
    falhas = Backend().rodar(str(tmp_path))
    assert len(falhas) == 2