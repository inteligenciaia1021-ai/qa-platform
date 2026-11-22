import sqlite3

import pytest

from qa_platform.knowledge.store import Store

PLAYBOOK = dict(
    o_que_aconteceu="Uma biblioteca necessária não está instalada.",
    por_que="O projeto usa a biblioteca requests, mas ela não foi instalada.",
    como_resolver="1. Abra o terminal. 2. Digite: pip install requests",
    como_confirmar="Rode o teste de novo. Ele deve passar sem esse erro.",
    se_nao_funcionou="Confira se o ambiente virtual (.venv) está ativo.",
)


@pytest.fixture
def store():
    s = Store(":memory:")
    yield s
    s.fechar()


def test_primeiro_registro_nao_e_repetido(store):
    assert store.registrar_bug("abc", "backend", "erro x") is False


def test_registro_repetido_incrementa_ocorrencias(store):
    store.registrar_bug("abc", "backend", "erro x")
    assert store.registrar_bug("abc", "backend", "erro x") is True
    assert store.buscar_bug("abc")["ocorrencias"] == 2


def test_bug_inexistente_retorna_none(store):
    assert store.buscar_bug("nao-existe") is None


def test_salvar_e_buscar_playbook(store):
    store.registrar_bug("abc", "backend", "erro x")
    store.salvar_playbook("abc", **PLAYBOOK)
    assert store.buscar_playbook("abc")["como_resolver"] == PLAYBOOK["como_resolver"]


def test_bug_sem_playbook_retorna_none(store):
    store.registrar_bug("abc", "backend", "erro x")
    assert store.buscar_playbook("abc") is None


def test_playbook_incompleto_e_recusado(store):
    store.registrar_bug("abc", "backend", "erro x")
    incompleto = {**PLAYBOOK, "como_resolver": ""}
    with pytest.raises(ValueError):
        store.salvar_playbook("abc", **incompleto)


def test_playbook_exige_bug_existente(store):
    with pytest.raises(sqlite3.IntegrityError):
        store.salvar_playbook("fantasma", **PLAYBOOK)