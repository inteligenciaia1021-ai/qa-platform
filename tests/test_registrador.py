from qa_platform.core.diagnostico import diagnosticar, procurar_playbook
from qa_platform.core.registrador import ler_campo, listar_sem_guia, registrar_guia
from qa_platform.knowledge.store import Store


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
    texto = ler_campo("Como resolver?", ler, lambda _t: None)
    assert texto == "1. Abra o terminal\n2. Digite o comando"


def test_campo_vazio_e_recusado():
    mensagens = []
    ler = _leitor(["", "texto", ""])
    assert ler_campo("Pergunta?", ler, mensagens.append) == "texto"
    assert any("obrigatório" in m for m in mensagens)


def test_registra_guia_completo():
    store = _store_com_dois_erros()
    bug = listar_sem_guia(store)[0]
    respostas = [
        "Aconteceu X", "",
        "Porque Y", "",
        "1. Faça Z", "2. Depois W", "",
        "Rode de novo", "",
        "Peça ajuda", "",
    ]
    registrar_guia(store, bug["fingerprint"], _leitor(respostas), lambda _t: None)
    guia = procurar_playbook(store, bug["fingerprint"], bug["mensagem"])
    assert guia["como_resolver"] == "1. Faça Z\n2. Depois W"
    assert listar_sem_guia(store) == []
    store.fechar()