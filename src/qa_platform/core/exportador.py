import re
from pathlib import Path

from qa_platform.core.diagnostico import procurar_playbook
from qa_platform.knowledge.store import Store

SECOES = (
    ("o_que_aconteceu", "O que aconteceu"),
    ("por_que", "Por que acontece"),
    ("como_resolver", "Como resolver"),
    ("como_confirmar", "Como confirmar que resolveu"),
    ("se_nao_funcionou", "Se não funcionou"),
)


def _nome_arquivo(bug: dict) -> str:
    modulo = re.sub(r"[^a-z0-9_-]", "", bug["modulo"].lower()) or "modulo"
    return f"{modulo}_{bug['fingerprint']}.md"


def _resumo(mensagem: str, limite: int = 80) -> str:
    texto = " ".join(mensagem.split())
    if len(texto) > limite:
        texto = texto[: limite - 1] + "…"
    # caracteres que quebrariam a tabela ou o link do índice
    for especial in ("|", "[", "]"):
        texto = texto.replace(especial, "\\" + especial)
    return texto


def _documento(bug: dict, playbook: dict | None) -> str:
    mensagem = bug["mensagem"].replace("```", "'''")
    linhas = [
        f"# Erro {bug['fingerprint']}",
        "",
        "```",
        mensagem,
        "```",
        "",
        f"- **Módulo:** {bug['modulo']}",
        f"- **Ocorrências:** {bug['ocorrencias']}",
        f"- **Primeira vez:** {bug['primeira_vez']}",
        f"- **Última vez:** {bug['ultima_vez']}",
        "",
        "## Guia de solução",
        "",
    ]
    if playbook is None:
        aviso = (
            "**Ainda não existe guia para este erro.** Quando descobrir a "
            "solução, registre-a na base de conhecimento para que ela apareça "
            "na próxima vez."
        )
        linhas += [aviso, ""]
        return "\n".join(linhas)
    for campo, titulo in SECOES:
        linhas += [f"### {titulo}", "", playbook[campo].replace("\n", "  \n"), ""]
    return "\n".join(linhas)


def exportar(store: Store, pasta: str = "contexto") -> int:
    """Escreve um .md por erro e um INDEX.md. Devolve quantos erros foram exportados."""
    destino = Path(pasta)
    destino.mkdir(parents=True, exist_ok=True)
    linhas = store.con.execute(
        "SELECT * FROM bugs ORDER BY ocorrencias DESC, ultima_vez DESC"
    ).fetchall()
    bugs = [dict(linha) for linha in linhas]

    tabela = []
    com_guia = 0
    for bug in bugs:
        playbook = procurar_playbook(store, bug["fingerprint"], bug["mensagem"])
        com_guia += playbook is not None
        nome = _nome_arquivo(bug)
        (destino / nome).write_text(_documento(bug, playbook), encoding="utf-8")
        tabela.append(
            f"| [{_resumo(bug['mensagem'])}]({nome}) | {bug['modulo']} "
            f"| {bug['ocorrencias']} | {'sim' if playbook else 'não'} |"
        )

    indice = [
        "# Memória de erros",
        "",
        f"{len(bugs)} erros registrados, {com_guia} com guia de solução.",
        "",
        "| Erro | Módulo | Vezes | Guia |",
        "|---|---|---|---|",
        *tabela,
        "",
    ]
    (destino / "INDEX.md").write_text("\n".join(indice), encoding="utf-8")
    return len(bugs)