from dataclasses import dataclass

from qa_platform.knowledge.catalogo import buscar_no_catalogo
from qa_platform.knowledge.catalogo_python import buscar_no_catalogo_python
from qa_platform.knowledge.fingerprint import gerar_fingerprint
from qa_platform.knowledge.store import Store


@dataclass
class Diagnostico:
    fingerprint: str
    ja_visto: bool
    ocorrencias: int
    playbook: dict | None


def _procurar_playbook(store: Store, fingerprint: str, mensagem: str) -> dict | None:
    # Ordem de prioridade: banco (guia salvo por você), catálogo do ruff,
    # catálogo de erros do Python.
    return (
        store.buscar_playbook(fingerprint)
        or buscar_no_catalogo(mensagem)
        or buscar_no_catalogo_python(mensagem)
    )


def diagnosticar(
    store: Store, modulo: str, mensagem: str, stack: str | None = None
) -> Diagnostico:
    fingerprint = gerar_fingerprint(modulo, mensagem)
    ja_visto = store.registrar_bug(fingerprint, modulo, mensagem, stack)
    bug = store.buscar_bug(fingerprint)
    playbook = _procurar_playbook(store, fingerprint, mensagem)
    return Diagnostico(
        fingerprint=fingerprint,
        ja_visto=ja_visto,
        ocorrencias=bug["ocorrencias"],
        playbook=playbook,
    )