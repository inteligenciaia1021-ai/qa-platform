from qa_platform.core.diagnostico import Diagnostico
from qa_platform.reporters.texto import formatar


def test_erro_novo_sem_playbook():
    texto = formatar(Diagnostico("abc123", False, 1, None))
    assert "primeira vez" in texto
    assert "Ainda não existe" in texto
    assert "abc123" in texto


def test_erro_repetido_com_playbook():
    playbook = {
        "o_que_aconteceu": "Algo falhou.",
        "por_que": "Por causa disso.",
        "como_resolver": "1. Faça aquilo.",
        "como_confirmar": "Rode de novo.",
        "se_nao_funcionou": "Peça ajuda.",
    }
    texto = formatar(Diagnostico("abc123", True, 3, playbook))
    assert "3 vezes" in texto
    assert "COMO RESOLVER" in texto
    assert "1. Faça aquilo." in texto