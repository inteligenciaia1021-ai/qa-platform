from qa_platform.core.diagnostico import procurar_playbook
from qa_platform.knowledge.store import CAMPOS_PLAYBOOK, Store

PERGUNTAS = {
    "o_que_aconteceu": "O QUE ACONTECEU? (explique em linguagem simples)",
    "por_que": "POR QUE ACONTECE? (a causa, sem termos técnicos)",
    "como_resolver": "COMO RESOLVER? (passos numerados, com os comandos exatos)",
    "como_confirmar": "COMO CONFIRMAR QUE RESOLVEU? (o que a pessoa deve ver)",
    "se_nao_funcionou": "SE NÃO FUNCIONOU, o que fazer?",
}


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


def ler_campo(pergunta: str, ler=input, mostrar=print) -> str:
    """Lê um campo de várias linhas. Termina com uma linha vazia."""
    while True:
        mostrar(f"\n{pergunta}")
        mostrar("(escreva quantas linhas precisar; termine com uma linha vazia)")
        linhas = []
        while True:
            linha = ler("> ")
            if not linha.strip():
                break
            linhas.append(linha.rstrip())
        if linhas:
            return "\n".join(linhas)
        mostrar("Este campo é obrigatório. Tente de novo.")


def registrar_guia(store: Store, fingerprint: str, ler=input, mostrar=print) -> None:
    # só salva depois de ter todos os campos: cancelar no meio não deixa guia pela metade
    campos = {c: ler_campo(PERGUNTAS[c], ler, mostrar) for c in CAMPOS_PLAYBOOK}
    store.salvar_playbook(fingerprint, **campos)