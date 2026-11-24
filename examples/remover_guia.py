import sys

from qa_platform.knowledge.store import Store

if len(sys.argv) < 2:
    sys.exit("Uso: python examples\\remover_guia.py TEXTO_DO_INICIO_DA_MENSAGEM")

inicio = sys.argv[1]
store = Store("knowledge.db")
resultado = store.con.execute(
    "DELETE FROM playbooks WHERE fingerprint IN "
    "(SELECT fingerprint FROM bugs WHERE mensagem LIKE ?)",
    (inicio + "%",),
)
store.con.commit()
print(f"{resultado.rowcount} guia(s) removido(s).")