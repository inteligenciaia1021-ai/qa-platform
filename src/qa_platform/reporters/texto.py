from qa_platform.core.diagnostico import Diagnostico


def formatar(d: Diagnostico) -> str:
    linhas = []

    if d.ja_visto:
        linhas.append(f"Este erro já ocorreu {d.ocorrencias} vezes.")
    else:
        linhas.append("Erro novo: é a primeira vez que ele aparece.")

    if d.playbook is None:
        linhas.append("Ainda não existe um guia de solução para este erro.")
        linhas.append(f"Código do erro: {d.fingerprint}")
        return "\n".join(linhas)

    p = d.playbook
    secoes = [
        ("O QUE ACONTECEU", p["o_que_aconteceu"]),
        ("POR QUE ACONTECE", p["por_que"]),
        ("COMO RESOLVER", p["como_resolver"]),
        ("COMO CONFIRMAR QUE RESOLVEU", p["como_confirmar"]),
        ("SE NÃO FUNCIONOU", p["se_nao_funcionou"]),
    ]
    for titulo, texto in secoes:
        linhas += ["", titulo, texto]
    return "\n".join(linhas)