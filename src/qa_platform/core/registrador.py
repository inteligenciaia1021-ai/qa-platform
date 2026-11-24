from qa_platform.core.diagnostico import procurar_playbook
from qa_platform.knowledge.store import CAMPOS_PLAYBOOK, Store

TAMANHO_CODIGO = 16
SAIR = "-"

PERGUNTAS = {
    "o_que_aconteceu": "O QUE ACONTECEU? (explique em linguagem simples)",
    "por_que": "POR QUE ACONTECE? (a causa, sem termos técnicos)",
    "como_resolver": "COMO RESOLVER? (passos numerados, com os comandos exatos)",
    "como_confirmar": "COMO CONFIRMAR QUE RESOLVEU? (o que a pessoa deve ver)",
    "se_nao_funcionou": "SE NÃO FUNCIONOU, o que fazer?",
}

TITULOS = {
    "o_que_aconteceu": "O QUE ACONTECEU",
    "por_que": "POR QUE ACONTECE",
    "como_resolver": "COMO RESOLVER",
    "como_confirmar": "COMO CONFIRMAR QUE RESOLVEU",
    "se_nao_funcionou": "SE NÃO FUNCIONOU",
}


class CanceladoError(Exception):
    """A pessoa desistiu de registrar o guia."""


def listar_sem_guia(store: Store, incluir_com_guia: bool = False) -> list[dict]:
    linhas = store.con.execute(
        "SELECT * FROM bugs ORDER BY ocorrencias DESC, ultima_vez DESC"
    ).fetchall()
    resultado = []
    for linha in linhas:
        bug = dict(linha)
        sem_guia = procurar_playbook(store, bug["fingerprint"], bug["mensagem"]) is None
        if incluir_com_guia or sem_guia:
            resultado.append(bug)
    return resultado


def escolher_erro(store: Store, bugs: list[dict], entrada: str) -> dict | None:
    """Aceita o número da lista ou o código do erro. Devolve None se não achar."""
    entrada = entrada.strip()
    if len(entrada) == TAMANHO_CODIGO:
        return store.buscar_bug(entrada.lower())
    if entrada.isdecimal() and 1 <= int(entrada) <= len(bugs):
        return bugs[int(entrada) - 1]
    return None


def confirmar(pergunta: str, ler=input, mostrar=print) -> bool:
    while True:
        resposta = ler(f"{pergunta} (s/n): ").strip().lower()
        if resposta in ("s", "sim"):
            return True
        if resposta in ("n", "nao", "não"):
            return False
        mostrar("Responda s (sim) ou n (não).")


def ler_campo(pergunta: str, ler=input, mostrar=print) -> str:
    """Lê um campo de várias linhas. Termina com uma linha vazia."""
    while True:
        mostrar(f"\n{pergunta}")
        mostrar(f"(termine com uma linha vazia; digite {SAIR} para desistir sem salvar)")
        linhas = []
        while True:
            linha = ler("> ")
            if linha.strip() == SAIR:
                raise CanceladoError
            if not linha.strip():
                break
            linhas.append(linha.rstrip())
        if linhas:
            return "\n".join(linhas)
        mostrar(f"Este campo é obrigatório. Se não souber, digite {SAIR} para desistir.")


def formatar_guia(campos: dict) -> str:
    partes = []
    for campo in CAMPOS_PLAYBOOK:
        partes += [TITULOS[campo], campos[campo], ""]
    return "\n".join(partes)


def registrar_guia(store: Store, bug: dict, ler=input, mostrar=print) -> bool:
    """Pergunta cada campo, mostra o guia e só salva com confirmação.

    Devolve True se o guia foi salvo.
    """
    try:
        if procurar_playbook(store, bug["fingerprint"], bug["mensagem"]) is not None:
            mostrar("\nEste erro já tem um guia. O seu vai substituí-lo.")
            if not confirmar("Continuar?", ler, mostrar):
                mostrar("Nada foi alterado.")
                return False
        campos = {c: ler_campo(PERGUNTAS[c], ler, mostrar) for c in CAMPOS_PLAYBOOK}
        mostrar("\n=== REVISE O GUIA ===\n")
        mostrar(formatar_guia(campos))
        if not confirmar("Salvar este guia?", ler, mostrar):
            mostrar("Nada foi salvo.")
            return False
    except CanceladoError:
        mostrar("\nVocê desistiu. Nada foi salvo.")
        return False
    store.salvar_playbook(bug["fingerprint"], **campos)
    return True