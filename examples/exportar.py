import sys

from qa_platform.core.exportador import exportar
from qa_platform.knowledge.store import Store

pasta = sys.argv[1] if len(sys.argv) > 1 else "contexto"
store = Store("knowledge.db")
total = exportar(store, pasta)
print(f"{total} erros exportados para a pasta '{pasta}'. Abra {pasta}/INDEX.md")