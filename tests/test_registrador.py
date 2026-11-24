from qa_platform.core.diagnostico import diagnosticar, procurar_playbook
from qa_platform.core.registrador import (
    confirmar,
    escolher_erro,
    ler_campo,
    listar_sem_guia,
    registrar_guia,
)
from qa_platform.knowledge.store import Store

RESPOSTAS = [
    "Aconteceu X", "",
    "Porque Y", "",
    "1. Faça Z", "2. Depois W", "",
    "Rode de novo", "",
    "Peça ajuda", "",
]


def _mudo(_texto):
    return None


def _leitor(respostas):
    itens = iter(respostas)
    return lambda _prompt="": next(itens)


def _store_com_dois_erros():
    store = Store(":memory:")
    diagnosticar(store, "code_quality", "F401: `os` imported but unused")
    diagnosticar(store, "backend", "RuntimeError: falha no pagamento")
    return store


def test_lista_so_erros_sem_guia():
    store = _store_com_dois_erros()
    bugs = listar_sem_guia(store)
    assert len(bugs) == 1
    assert bugs[0]["mensagem"].startswith("RuntimeError")
    store.fechar()


def test_todos_inclui_erros_que_ja_tem_guia():
    store = _store_com_dois_erros()
    assert len(listar_sem_guia(store, incluir_com_guia=True)) == 2
    store.fechar()


def test_campo_aceita_varias_linhas():
    ler = _leitor(["1. Abra o terminal", "2. Digite o comando", ""])
    texto = ler_campo("Como resolver?", ler, _mudo)
    assert texto == "1. Abra o terminal\n2. Digite o comando"


def test_campo_vazio_e_recusado():
    mensagens = []
    ler = _leitor(["", "texto", ""])
    assert ler_campo("Pergunta?", ler, mensagens.append) == "texto"
    assert any("obrigatório" in m for m in mensagens)


def test_registra_guia_completo():
    store = _store_com_dois_erros()
    bug = listar_sem_guia(store)[0]
    ler = _leitor([*RESPOSTAS, "s"])
    assert registrar_guia(store, bug, ler, _mudo) is True
    guia = procurar_playbook(store, bug["fingerprint"], bug["mensagem"])
    assert guia["como_resolver"] == "1. Faça Z\n2. Depois W"
    assert listar_sem_guia(store) == []
    store.fechar()


def test_desistir_com_traco_nao_salva():
    store = _store_com_dois_erros()
    bug = listar_sem_guia(store)[0]
    ler = _leitor(["Aconteceu X", "", "-"])
    assert registrar_guia(store, bug, ler, _mudo) is False
    assert store.buscar_playbook(bug["fingerprint"]) is None
    store.fechar()


def test_responder_nao_na_revisao_nao_salva():
    store = _store_com_dois_erros()
    bug = listar_sem_guia(store)[0]
    ler = _leitor([*RESPOSTAS, "n"])
    assert registrar_guia(store, bug, ler, _mudo) is False
    assert store.buscar_playbook(bug["fingerprint"]) is None
    store.fechar()


def test_erro_com_guia_pede_confirmacao_e_respeita_o_nao():
    store = Store(":memory:")
    d = diagnosticar(store, "code_quality", "F401: `os` imported but unused")
    bug = store.buscar_bug(d.fingerprint)
    assert registrar_guia(store, bug, _leitor(["n"]), _mudo) is False
    assert store.buscar_playbook(d.fingerprint) is None
    store.fechar()


def test_erro_com_guia_e_substituido_se_confirmar():
    store = Store(":memory:")
    d = diagnosticar(store, "code_quality", "F401: `os` imported but unused")
    bug = store.buscar_bug(d.fingerprint)
    ler = _leitor(["s", *RESPOSTAS, "s"])
    assert registrar_guia(store, bug, ler, _mudo) is True
    guia = store.buscar_playbook(d.fingerprint)
    assert guia["como_resolver"] == "1. Faça Z\n2. Depois W"
    store.fechar()


def test_confirmar_repete_ate_resposta_valida():
    mensagens = []
    ler = _leitor(["talvez", "", "SIM"])
    assert confirmar("Salvar?", ler, mensagens.append) is True
    assert len(mensagens) == 2


def test_escolher_por_numero():
    store = _store_com_dois_erros()
    bugs = listar_sem_guia(store, incluir_com_guia=True)
    assert escolher_erro(store, bugs, "1") == bugs[0]
    assert escolher_erro(store, bugs, " 2 ") == bugs[1]
    store.fechar()


def test_escolher_por_codigo_com_maiusculas_ou_minusculas():
    store = _store_com_dois_erros()
    bugs = listar_sem_guia(store, incluir_com_guia=True)
    codigo = bugs[0]["fingerprint"]
    assert escolher_erro(store, bugs, codigo)["fingerprint"] == codigo
    assert escolher_erro(store, bugs, codigo.upper()) is not None
    store.fechar()


def test_escolher_recusa_entradas_invalidas():
    store = _store_com_dois_erros()
    bugs = listar_sem_guia(store, incluir_com_guia=True)
    invalidas = ["banana", "0", "-1", "999", "2.5", "", "   ", "0123456789abcdef"]
    for entrada in invalidas:
        assert escolher_erro(store, bugs, entrada) is None, entrada
    store.fechar()