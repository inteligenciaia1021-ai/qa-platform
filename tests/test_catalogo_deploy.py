from qa_platform.knowledge.catalogo_deploy import (
    CATALOGO_DEPLOY,
    buscar_no_catalogo_deploy,
)

CAMPOS = (
    "o_que_aconteceu",
    "por_que",
    "como_resolver",
    "como_confirmar",
    "se_nao_funcionou",
)


def test_todos_os_playbooks_de_deploy_estao_completos():
    for prefixo, playbook in CATALOGO_DEPLOY.items():
        for campo in CAMPOS:
            assert playbook.get(campo), f"{prefixo} sem {campo}"


def test_encontra_playbook_pelo_inicio_da_mensagem():
    achado = buscar_no_catalogo_deploy("Container roda como administrador (root)")
    assert achado is not None
    assert "USER" in achado["como_resolver"]


def test_mensagem_desconhecida_nao_tem_playbook():
    assert buscar_no_catalogo_deploy("Outra coisa qualquer") is None