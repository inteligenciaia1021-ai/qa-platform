from qa_platform.core.diagnostico import diagnosticar
from qa_platform.knowledge.store import Store
from qa_platform.reporters.texto import formatar

store = Store("knowledge.db")
erro = "ModuleNotFoundError: No module named 'requests'"

diagnostico = diagnosticar(store, "backend", erro)
print(formatar(diagnostico))

if diagnostico.playbook is None:
    store.salvar_playbook(
        diagnostico.fingerprint,
        o_que_aconteceu="Uma biblioteca necessária não está instalada.",
        por_que="O projeto usa a biblioteca requests, mas ela não foi instalada.",
        como_resolver="1. Abra o terminal.\n2. Digite: pip install requests",
        como_confirmar="Rode o teste de novo. Ele deve passar sem esse erro.",
        se_nao_funcionou="Confira se o ambiente virtual (.venv) está ativo.",
    )
    print("\n[Guia de solução salvo. Rode o demo de novo.]")