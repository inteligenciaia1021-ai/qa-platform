from qa_platform.knowledge.catalogo_seguranca import (
    CATALOGO_PREFIXOS,
    CATALOGO_SEGURANCA,
    buscar_no_catalogo_seguranca,
)

CAMPOS = (
    "o_que_aconteceu",
    "por_que",
    "como_resolver",
    "como_confirmar",
    "se_nao_funcionou",
)


def test_todos_os_playbooks_de_seguranca_estao_completos():
    todos = {**CATALOGO_SEGURANCA, **CATALOGO_PREFIXOS}
    for chave, playbook in todos.items():
        for campo in CAMPOS:
            assert playbook.get(campo), f"{chave} sem {campo}"


def test_encontra_playbook_pelo_codigo_do_bandit():
    achado = buscar_no_catalogo_seguranca("B105: Possible hardcoded password [gravidade LOW]")
    assert achado is not None
    assert "variável de ambiente" in achado["como_resolver"]


def test_dependencia_vulneravel_traz_o_nome_do_pacote():
    achado = buscar_no_catalogo_seguranca(
        "Dependência vulnerável: requests 2.19.0 (PYSEC-2018-28) - corrigido em: 2.20.0"
    )
    assert "pip install --upgrade requests" in achado["como_resolver"]
    assert "{pacote}" not in achado["como_resolver"]


def test_mensagem_desconhecida_nao_tem_playbook():
    assert buscar_no_catalogo_seguranca("Outra coisa qualquer") is None
    assert buscar_no_catalogo_seguranca("B999: algo novo") is None