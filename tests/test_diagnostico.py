import pytest

from qa_platform.core.diagnostico import diagnosticar
from qa_platform.knowledge.store import Store

PLAYBOOK = {
    "o_que_aconteceu": "Falha de exemplo.",
    "por_que": "Causa de exemplo.",
    "como_resolver": "1. Faça isto.",
    "como_confirmar": "Rode de novo.",
    "se_nao_funcionou": "Peça ajuda.",
}


@pytest.fixture
def store():
    s = Store(":memory:")
    yield s
    s.fechar()


def test_primeiro_erro_nao_foi_visto(store):
    d = diagnosticar(store, "backend", "Falha na linha 10")
    assert d.ja_visto is False
    assert d.ocorrencias == 1
    assert d.playbook is None


def test_erro_parecido_e_reconhecido(store):
    diagnosticar(store, "backend", "Falha na linha 10")
    d = diagnosticar(store, "backend", "Falha na linha 99")
    assert d.ja_visto is True
    assert d.ocorrencias == 2


def test_erro_com_playbook_traz_a_solucao(store):
    primeiro = diagnosticar(store, "backend", "Falha na linha 10")
    store.salvar_playbook(primeiro.fingerprint, **PLAYBOOK)
    d = diagnosticar(store, "backend", "Falha na linha 55")
    assert d.playbook["como_resolver"] == PLAYBOOK["como_resolver"]