import sys

from qa_platform.core.exportador import exportar
from qa_platform.core.registrador import listar_sem_guia, registrar_guia
from qa_platform.knowledge.store import Store

TAMANHO_CODIGO = 16


def _linha(bug: dict) -> str:
    resumo = " ".join(bug["mensagem"].split())[:100]
    return f"[{bug['modulo']}] {resumo} ({bug['ocorrencias']}x)"


def _escolher(store: Store, bugs: list[dict], escolha: str) -> dict | None:
    """Aceita o número da lista ou o código do erro."""
    if len(escolha) == TAMANHO_CODIGO:
        return store.buscar_bug(escolha.lower())
    if escolha.isdecimal() and 1 <= int(escolha) <= len(bugs):
        return bugs[int(escolha) - 1]
    return None


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
        bug = _escolher(store, bugs, escolha)
        if bug is not None:
            break
        print("Não encontrei. Digite o número da lista (ex.: 1) ou o código do erro.")

    print(f"\nVocê vai escrever o guia para:\n{_linha(bug)}")
    registrar_guia(store, bug["fingerprint"])
    total = exportar(store)
    print(f"\nGuia salvo. A pasta 'contexto' foi atualizada ({total} erros).")


try:
    main()
except (EOFError, KeyboardInterrupt):
    print("\nCancelado. Nada foi salvo.")