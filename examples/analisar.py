import sys

from qa_platform.core.executor import executar
from qa_platform.knowledge.store import Store
from qa_platform.modules.code_quality import CodeQuality
from qa_platform.reporters.texto import formatar

caminho = sys.argv[1] if len(sys.argv) > 1 else "."
store = Store("knowledge.db")

resultados = executar(store, CodeQuality(), caminho)
if not resultados:
    print("Nenhum problema encontrado.")

for falha, diagnostico in resultados:
    print(f"\n=== {falha.arquivo}:{falha.linha} ===")
    print(falha.mensagem)
    print(formatar(diagnostico))