from qa_platform.core.diagnostico import diagnosticar
from qa_platform.knowledge.catalogo import CATALOGO, buscar_no_catalogo, extrair_codigo
from qa_platform.knowledge.store import Store

CAMPOS = (
    "o_que_aconteceu",
    "por_que",
    "como_resolver",
    "como_confirmar",
    "se_nao_funcionou",
)


def test_todos_os_playbooks_do_catalogo_estao_completos():
    for codigo, playbook in CATALOGO.items():
        for campo in CAMPOS:
            assert playbook.get(campo), f"{codigo} sem {campo}"


def test_extrai_codigo_da_mensagem():
    assert extrair_codigo("F401: `os` imported but unused") == "F401"
    assert extrair_codigo("Erro qualquer") is None


def test_codigo_desconhecido_nao_tem_playbook():
    assert buscar_no_catalogo("Z999: algo") is None


def test_diagnostico_usa_o_catalogo_em_erro_novo():
    store = Store(":memory:")
    d = diagnosticar(store, "code_quality", "F401: `os` imported but unused")
    assert d.ja_visto is False
    assert "import" in d.playbook["como_resolver"]
    store.fechar()


def test_playbook_do_banco_tem_prioridade_sobre_o_catalogo():
    store = Store(":memory:")
    mensagem = "F401: `os` imported but unused"
    primeiro = diagnosticar(store, "code_quality", mensagem)
    store.salvar_playbook(
        primeiro.fingerprint,
        o_que_aconteceu="Versão da equipe.",
        por_que="x",
        como_resolver="Faça do jeito da equipe.",
        como_confirmar="x",
        se_nao_funcionou="x",
    )
    d = diagnosticar(store, "code_quality", mensagem)
    assert d.playbook["como_resolver"] == "Faça do jeito da equipe."
    store.fechar()