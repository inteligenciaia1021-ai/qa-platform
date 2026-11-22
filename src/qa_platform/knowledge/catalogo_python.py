import re

_ERRO_PYTHON = re.compile(r"^([A-Za-z]+(?:Error|Exception))\b")
_MODULO_AUSENTE = re.compile(r"No module named '([^'.]+)")

CATALOGO_PYTHON = {
    "ModuleNotFoundError": {
        "o_que_aconteceu": "O programa tentou usar a biblioteca '{biblioteca}', "
        "mas ela não está instalada neste computador.",
        "por_que": "Bibliotecas externas precisam ser instaladas uma vez em cada "
        "ambiente. É comum faltar depois de baixar um projeto novo ou de criar "
        "um ambiente virtual novo.",
        "como_resolver": "1. Abra o terminal na pasta do projeto.\n"
        "2. Confirme que o ambiente virtual está ativo (aparece (.venv) no "
        "início da linha).\n"
        "3. Digite: pip install {biblioteca}",
        "como_confirmar": "Rode o programa ou os testes de novo. O erro deve sumir.",
        "se_nao_funcionou": "Alguns nomes de import são diferentes do nome de "
        "instalação (por exemplo, 'cv2' se instala com 'pip install "
        "opencv-python'). Procure '{biblioteca} pip install' na internet para "
        "achar o nome certo. Se o projeto tem um arquivo requirements.txt, "
        "rode: pip install -r requirements.txt",
    },
    "AssertionError": {
        "o_que_aconteceu": "Um teste verificou uma condição e ela era falsa.",
        "por_que": "O resultado do código foi diferente do que o teste esperava. "
        "Ou o código tem um defeito, ou o teste está com a expectativa errada.",
        "como_resolver": "1. Rode: pytest -v  e veja a linha 'assert' que falhou, "
        "com os valores comparados.\n"
        "2. Compare o valor obtido com o esperado.\n"
        "3. Se o esperado está certo, corrija o código testado.\n"
        "4. Se o código está certo, corrija o valor esperado no teste.",
        "como_confirmar": "Rode: pytest  O teste deve passar.",
        "se_nao_funcionou": "Não ajuste o teste só para ele passar sem entender "
        "por que falhou. Se tiver dúvida de qual lado está errado, peça ajuda "
        "a quem desenvolve.",
    },
    "ZeroDivisionError": {
        "o_que_aconteceu": "O código tentou dividir um número por zero.",
        "por_que": "O valor usado como divisor chegou como 0, o que a matemática "
        "não permite.",
        "como_resolver": "1. Vá até a linha da divisão indicada no erro.\n"
        "2. Descubra de onde vem o divisor e por que ele é zero.\n"
        "3. Antes de dividir, verifique: if divisor != 0:",
        "como_confirmar": "Rode o programa ou os testes de novo. O erro deve sumir.",
        "se_nao_funcionou": "Se o zero é um caso válido, decida o que o programa "
        "deve devolver nesse caso (por exemplo, 0 ou uma mensagem de aviso).",
    },
    "KeyError": {
        "o_que_aconteceu": "O código procurou uma chave que não existe em um "
        "dicionário.",
        "por_que": "A chave pode estar escrita diferente (maiúsculas contam) ou "
        "o dado não chegou como esperado.",
        "como_resolver": "1. Veja o nome da chave na mensagem de erro.\n"
        "2. Confira se está escrita exatamente igual à usada no dicionário.\n"
        "3. Para não quebrar quando a chave faltar, use: "
        "dicionario.get(\"chave\")",
        "como_confirmar": "Rode o programa ou os testes de novo. O erro deve sumir.",
        "se_nao_funcionou": "Imprima o dicionário (print(dicionario)) para ver "
        "quais chaves ele realmente tem.",
    },
    "IndexError": {
        "o_que_aconteceu": "O código pediu uma posição que não existe em uma lista.",
        "por_que": "A lista é menor do que o código esperava. Lembre que a "
        "contagem começa em 0: uma lista com 3 itens tem as posições 0, 1 e 2.",
        "como_resolver": "1. Vá até a linha indicada.\n"
        "2. Confira o tamanho da lista com len(lista).\n"
        "3. Ajuste a posição pedida, ou verifique antes: if len(lista) > posicao:",
        "como_confirmar": "Rode o programa ou os testes de novo. O erro deve sumir.",
        "se_nao_funcionou": "Se a lista veio vazia, descubra por que os dados "
        "não chegaram.",
    },
    "TypeError": {
        "o_que_aconteceu": "O código misturou tipos de dados que não combinam.",
        "por_que": "Exemplo clássico: somar um texto com um número, ou chamar uma "
        "função com a quantidade errada de valores.",
        "como_resolver": "1. Leia a mensagem: ela diz quais tipos se misturaram.\n"
        "2. Vá até a linha indicada.\n"
        "3. Converta o valor: int(\"5\") vira número, str(5) vira texto.\n"
        "4. Se for chamada de função, confira se passou todos os valores pedidos.",
        "como_confirmar": "Rode o programa ou os testes de novo. O erro deve sumir.",
        "se_nao_funcionou": "Imprima o tipo do valor suspeito: print(type(valor)).",
    },
    "AttributeError": {
        "o_que_aconteceu": "O código tentou usar algo que o objeto não tem.",
        "por_que": "Pode ser erro de digitação no nome, ou o objeto ser outra "
        "coisa do que se esperava. Com frequência o valor é None, porque uma "
        "função não devolveu nada.",
        "como_resolver": "1. Leia a mensagem: ela diz qual objeto e qual nome "
        "faltam.\n"
        "2. Confira a escrita do nome.\n"
        "3. Se a mensagem fala de 'NoneType', descubra por que o valor ficou None.",
        "como_confirmar": "Rode o programa ou os testes de novo. O erro deve sumir.",
        "se_nao_funcionou": "Veja o que o objeto realmente tem: print(dir(objeto)).",
    },
    "NameError": {
        "o_que_aconteceu": "O código usa um nome que ainda não foi definido.",
        "por_que": "Erro de digitação, ou o nome foi usado antes de ser criado, "
        "ou falta um import.",
        "como_resolver": "1. Veja o nome apontado na mensagem.\n"
        "2. Confira se está escrito igual ao original.\n"
        "3. Confirme que ele é criado antes da linha que o usa.\n"
        "4. Se vem de uma biblioteca, adicione o import no topo do arquivo.",
        "como_confirmar": "Rode o programa ou os testes de novo. O erro deve sumir.",
        "se_nao_funcionou": "Procure o nome no projeto inteiro (Ctrl+Shift+F no "
        "VS Code).",
    },
    "FileNotFoundError": {
        "o_que_aconteceu": "O programa tentou abrir um arquivo que não existe "
        "naquele lugar.",
        "por_que": "O caminho está errado, o arquivo foi movido, ou o programa "
        "está rodando em outra pasta.",
        "como_resolver": "1. Veja o caminho do arquivo na mensagem.\n"
        "2. Confira se o arquivo existe nesse lugar.\n"
        "3. No terminal, confirme a pasta atual com: pwd\n"
        "4. Corrija o caminho ou mova o arquivo.",
        "como_confirmar": "Rode o programa ou os testes de novo. O erro deve sumir.",
        "se_nao_funcionou": "Procure o arquivo pelo nome (Ctrl+P no VS Code) "
        "para descobrir onde ele realmente está.",
    },
    "SyntaxError": {
        "o_que_aconteceu": "O código tem um erro de escrita e o Python não "
        "consegue nem começar a rodá-lo.",
        "por_que": "Quase sempre é um parêntese, colchete ou aspas que foi aberto "
        "e não fechado, ou falta dois-pontos no fim de uma linha.",
        "como_resolver": "1. Vá até a linha indicada.\n"
        "2. Olhe também a linha ANTERIOR: o erro real muitas vezes está lá.\n"
        "3. Confira se todo ( [ { \" ' aberto foi fechado.\n"
        "4. Confira se if, for, def e class terminam com dois-pontos.",
        "como_confirmar": "Rode o programa ou os testes de novo. O erro deve sumir.",
        "se_nao_funcionou": "Desfaça a última alteração (Ctrl+Z) e refaça com "
        "calma, uma mudança por vez.",
    },
}


def extrair_erro_python(mensagem: str) -> str | None:
    if mensagem.startswith("assert"):
        return "AssertionError"
    achado = _ERRO_PYTHON.match(mensagem)
    return achado.group(1) if achado else None


def buscar_no_catalogo_python(mensagem: str) -> dict | None:
    modelo = CATALOGO_PYTHON.get(extrair_erro_python(mensagem))
    if modelo is None:
        return None
    achado = _MODULO_AUSENTE.search(mensagem)
    biblioteca = achado.group(1) if achado else "NOME_DA_BIBLIOTECA"
    return {c: texto.replace("{biblioteca}", biblioteca) for c, texto in modelo.items()}