import sys

from qa_platform.core.exportador import exportar
from qa_platform.core.registrador import escolher_erro, listar_sem_guia, registrar_guia
from qa_platform.knowledge.store import Store


def _linha(bug: dict) -> str:
    resumo = " ".join(bug["mensagem"].split())[:100]
    return f"[{bug['modulo']}] {resumo} ({bug['ocorrencias']}x)"


def main() -> None:
    store = Store("knowledge.db")
    bugs = listar_sem_guia(store, incluir_com_guia="--todos" in sys.argv)
    if not bugs:
        print("Nenhum erro sem guia. Para reescrever um guia existente, use: --todos")
        return

    print("Erros registrados:\n")
    for numero, bug in enumerate(bugs, start=1):
        print(f"{numero}. {_linha(bug)}")

    while True:
        escolha = input("\nNúmero da lista ou código do erro (Enter para sair): ").strip()
        if not escolha:
            return
        bug = escolher_erro(store, bugs, escolha)
        if bug is not None:
            break
        print("Não encontrei. Digite o número da lista (ex.: 1) ou o código do erro.")

    print(f"\nVocê vai escrever o guia para:\n{_linha(bug)}")
    if registrar_guia(store, bug):
        total = exportar(store)
        print(f"\nGuia salvo. A pasta 'contexto' foi atualizada ({total} erros).")


try:
    main()
except (EOFError, KeyboardInterrupt):
    print("\nCancelado. Nada foi salvo.")