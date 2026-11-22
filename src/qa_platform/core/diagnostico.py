from dataclasses import dataclass

from qa_platform.knowledge.fingerprint import gerar_fingerprint
from qa_platform.knowledge.store import Store


@dataclass
class Diagnostico:
    fingerprint: str
    ja_visto: bool
    ocorrencias: int
    playbook: dict | None


def diagnosticar(store: Store, modulo: str, mensagem: str, stack: str | None = None) -> Diagnostico:
    fingerprint = gerar_fingerprint(modulo, mensagem)
    ja_visto = store.registrar_bug(fingerprint, modulo, mensagem, stack)
    bug = store.buscar_bug(fingerprint)
    return Diagnostico(
        fingerprint=fingerprint,
        ja_visto=ja_visto,
        ocorrencias=bug["ocorrencias"],
        playbook=store.buscar_playbook(fingerprint),
    )