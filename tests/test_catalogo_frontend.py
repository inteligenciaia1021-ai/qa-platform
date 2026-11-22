from qa_platform.knowledge.catalogo_frontend import (
    CATALOGO_FRONTEND,
    buscar_no_catalogo_frontend,
)

CAMPOS = (
    "o_que_aconteceu",
    "por_que",
    "como_resolver",
    "como_confirmar",
    "se_nao_funcionou",
)


def test_todos_os_playbooks_frontend_estao_completos():
    for prefixo, playbook in CATALOGO_FRONTEND.items():
        for campo in CAMPOS:
            assert playbook.get(campo), f"{prefixo} sem {campo}"


def test_encontra_playbook_pelo_inicio_da_mensagem():
    achado = buscar_no_catalogo_frontend("Recurso não encontrado (HTTP 404): http://x/y.png")
    assert achado is not None
    assert "caminho" in achado["como_resolver"]


def test_mensagem_desconhecida_nao_tem_playbook():
    assert buscar_no_catalogo_frontend("Outra coisa qualquer") is None