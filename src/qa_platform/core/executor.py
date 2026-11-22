from qa_platform.core.diagnostico import Diagnostico, diagnosticar
from qa_platform.knowledge.store import Store
from qa_platform.modules.base import Falha, Modulo


def executar(store: Store, modulo: Modulo, caminho: str) -> list[tuple[Falha, Diagnostico]]:
    return [
        (falha, diagnosticar(store, falha.modulo, falha.mensagem))
        for falha in modulo.rodar(caminho)
    ]