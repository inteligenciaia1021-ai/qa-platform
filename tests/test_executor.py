from qa_platform.core.executor import executar
from qa_platform.knowledge.store import Store
from qa_platform.modules.base import Falha


class ModuloFalso:
    nome = "falso"

    def rodar(self, caminho):
        return [
            Falha("falso", "Erro na linha 3", "a.py", 3),
            Falha("falso", "Erro na linha 8", "b.py", 8),
        ]


def test_falhas_parecidas_viram_o_mesmo_bug():
    store = Store(":memory:")
    resultados = executar(store, ModuloFalso(), ".")
    assert len(resultados) == 2
    assert resultados[0][1].fingerprint == resultados[1][1].fingerprint
    assert resultados[1][1].ocorrencias == 2
    store.fechar()