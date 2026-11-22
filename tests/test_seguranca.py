import json

from qa_platform.modules.seguranca import Seguranca, _ler_pip_audit


def test_detecta_senha_escrita_no_codigo(tmp_path):
    (tmp_path / "app.py").write_text('password = "abc123"\n')
    falhas = Seguranca().rodar(str(tmp_path))
    assert len(falhas) == 1
    assert falhas[0].mensagem.startswith("B105")
    assert "abc123" not in falhas[0].mensagem


def test_detecta_eval(tmp_path):
    (tmp_path / "app.py").write_text('resultado = eval("1 + 1")\n')
    falhas = Seguranca().rodar(str(tmp_path))
    assert any(f.mensagem.startswith("B307") for f in falhas)


def test_codigo_limpo_nao_gera_falhas(tmp_path):
    (tmp_path / "ok.py").write_text("x = 1\n")
    assert Seguranca().rodar(str(tmp_path)) == []


def test_assert_em_testes_nao_e_reportado(tmp_path):
    (tmp_path / "test_ok.py").write_text("def test_a():\n    assert 1 == 1\n")
    assert Seguranca().rodar(str(tmp_path)) == []


def test_le_resultado_do_pip_audit():
    texto = json.dumps(
        {
            "dependencies": [
                {
                    "name": "requests",
                    "version": "2.19.0",
                    "vulns": [
                        {"id": "PYSEC-2018-28", "fix_versions": ["2.20.0"], "aliases": []}
                    ],
                },
                {"name": "idna", "version": "3.7", "vulns": []},
            ]
        }
    )
    falhas = _ler_pip_audit(texto, "requirements.txt")
    assert len(falhas) == 1
    assert "requests 2.19.0" in falhas[0].mensagem
    assert "2.20.0" in falhas[0].mensagem


def test_dependencias_sem_vulnerabilidade_nao_geram_falha():
    texto = json.dumps({"dependencies": [{"name": "idna", "version": "3.7", "vulns": []}]})
    assert _ler_pip_audit(texto, "requirements.txt") == []


def test_vulnerabilidades_repetidas_viram_um_alerta_so():
    texto = json.dumps(
        {
            "dependencies": [
                {
                    "name": "urllib3",
                    "version": "1.23",
                    "vulns": [
                        {"id": "PYSEC-1", "fix_versions": ["1.24.2"]},
                        {"id": "PYSEC-1", "fix_versions": ["1.24.2"]},
                        {"id": "PYSEC-2", "fix_versions": ["1.26.19", "2.2.2"]},
                        {"id": "PYSEC-3", "fix_versions": ["2.6.0"]},
                    ],
                }
            ]
        }
    )
    falhas = _ler_pip_audit(texto, "requirements.txt")
    assert len(falhas) == 1
    assert "2.6.0" in falhas[0].mensagem
    assert "3 falhas" in falhas[0].mensagem


def test_vulnerabilidade_sem_correcao_e_informada():
    texto = json.dumps(
        {
            "dependencies": [
                {
                    "name": "antiga",
                    "version": "0.1",
                    "vulns": [{"id": "PYSEC-9", "fix_versions": []}],
                }
            ]
        }
    )
    falhas = _ler_pip_audit(texto, "requirements.txt")
    assert "sem versão corrigida" in falhas[0].mensagem