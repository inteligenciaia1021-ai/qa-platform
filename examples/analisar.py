import sys

from qa_platform.core.executor import executar
from qa_platform.knowledge.store import Store
from qa_platform.modules.backend import Backend
from qa_platform.modules.code_quality import CodeQuality
from qa_platform.modules.deploy import Deploy
from qa_platform.modules.frontend import Frontend
from qa_platform.modules.seguranca import Seguranca
from qa_platform.reporters.texto import formatar

MODULOS = {
    "code_quality": CodeQuality,
    "backend": Backend,
    "frontend": Frontend,
    "security": Seguranca,
    "deploy": Deploy,
}

caminho = sys.argv[1] if len(sys.argv) > 1 else "."
nome = sys.argv[2] if len(sys.argv) > 2 else "code_quality"

if nome not in MODULOS:
    sys.exit(f"Módulo desconhecido: {nome}. Opções: {', '.join(MODULOS)}")

store = Store("knowledge.db")
resultados = executar(store, MODULOS[nome](), caminho)
if not resultados:
    print("Nenhum problema encontrado.")

for falha, diagnostico in resultados:
    print(f"\n=== {falha.arquivo or '-'}:{falha.linha or '-'} ===")
    print(falha.mensagem)
    print(formatar(diagnostico))