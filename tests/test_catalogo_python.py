from qa_platform.knowledge.catalogo_python import (
    CATALOGO_PYTHON,
    buscar_no_catalogo_python,
    extrair_erro_python,
)

CAMPOS = (
    "o_que_aconteceu",
    "por_que",
    "como_resolver",
    "como_confirmar",
    "se_nao_funcionou",
)


def test_todos_os_playbooks_python_estao_completos():
    for erro, playbook in CATALOGO_PYTHON.items():
        for campo in CAMPOS:
            assert playbook.get(campo), f"{erro} sem {campo}"


def test_extrai_tipo_de_erro_python():
    assert extrair_erro_python("ZeroDivisionError: division by zero") == "ZeroDivisionError"
    assert extrair_erro_python("Erro qualquer") is None


def test_assert_do_pytest_vira_assertion_error():
    assert extrair_erro_python("assert (1 + 1) == 3") == "AssertionError"


def test_biblioteca_ausente_aparece_no_passo_a_passo():
    playbook = buscar_no_catalogo_python("ModuleNotFoundError: No module named 'pandas'")
    assert "pip install pandas" in playbook["como_resolver"]
    assert all("{biblioteca}" not in texto for texto in playbook.values())


def test_erro_desconhecido_nao_tem_playbook():
    assert buscar_no_catalogo_python("MeuErroInventadoError: algo") is None