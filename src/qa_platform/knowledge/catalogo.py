import re

_CODIGO = re.compile(r"^([A-Z]+[0-9]+):")

CATALOGO = {
    "F401": {
        "o_que_aconteceu": "O código importa algo que nunca é usado.",
        "por_que": "Sobrou de uma versão anterior ou foi importado por precaução. "
        "Deixa o código mais confuso e mais lento para carregar.",
        "como_resolver": "1. Abra o arquivo e vá até a linha indicada.\n"
        "2. Apague essa linha de import.\n"
        "Atalho: no terminal, digite: ruff check --fix .",
        "como_confirmar": "Rode: ruff check .  O aviso F401 deve sumir.",
        "se_nao_funcionou": "Se o arquivo se chama __init__.py, o import pode ser "
        "intencional (serve para expor algo ao resto do projeto). "
        "Nesse caso, não apague e peça ajuda a quem desenvolve.",
    },
    "F841": {
        "o_que_aconteceu": "Uma variável recebe um valor, mas nunca é usada depois.",
        "por_que": "Provavelmente é sobra de código antigo, ou a variável deveria "
        "ser usada mais adiante e foi esquecida.",
        "como_resolver": "1. Vá até a linha indicada.\n"
        "2. Se a variável não é necessária, apague a linha.\n"
        "3. Se o valor vem de uma chamada de função (ex.: x = buscar()), "
        "mantenha a chamada e apague só o 'x = '.\n"
        "4. Se ela deveria ser usada, use-a onde faltou.",
        "como_confirmar": "Rode: ruff check .  O aviso F841 deve sumir.",
        "se_nao_funcionou": "Se não tiver certeza do que a variável fazia, "
        "não apague: peça ajuda a quem desenvolve.",
    },
    "F821": {
        "o_que_aconteceu": "O código usa um nome que não existe.",
        "por_que": "Quase sempre é erro de digitação, ou falta um import.",
        "como_resolver": "1. Veja o nome apontado na mensagem.\n"
        "2. Confira se está escrito igual ao original (maiúsculas e minúsculas contam).\n"
        "3. Se o nome vem de outra biblioteca, adicione o import no topo do arquivo.",
        "como_confirmar": "Rode: ruff check .  O aviso F821 deve sumir.",
        "se_nao_funcionou": "O nome pode ter sido removido de outro arquivo. "
        "Procure por ele no projeto (Ctrl+Shift+F no VS Code).",
    },
    "F811": {
        "o_que_aconteceu": "Duas coisas diferentes foram definidas com o mesmo nome.",
        "por_que": "A segunda definição apaga a primeira sem avisar. "
        "Costuma ser função duplicada ou import repetido.",
        "como_resolver": "1. Veja as duas linhas citadas.\n"
        "2. Se for repetição acidental, apague uma delas.\n"
        "3. Se forem coisas diferentes, dê nomes diferentes a cada uma.",
        "como_confirmar": "Rode: ruff check .  O aviso F811 deve sumir.",
        "se_nao_funcionou": "Em testes, funções com o mesmo nome fazem um dos "
        "testes nunca rodar. Renomeie para que todos rodem.",
    },
    "F541": {
        "o_que_aconteceu": "Um texto foi marcado como f-string, mas não usa nenhuma {variável}.",
        "por_que": "O 'f' antes das aspas só é necessário quando há {algo} dentro do texto.",
        "como_resolver": "1. Vá até a linha indicada.\n"
        "2. Apague a letra f que fica antes das aspas.",
        "como_confirmar": "Rode: ruff check .  O aviso F541 deve sumir.",
        "se_nao_funcionou": "Se você queria mostrar uma variável, coloque-a entre "
        "chaves dentro do texto, por exemplo: f\"Olá, {nome}\".",
    },
    "E722": {
        "o_que_aconteceu": "O código usa 'except:' sem dizer qual erro quer tratar.",
        "por_que": "Isso captura até erros que não deveria (como Ctrl+C), "
        "escondendo problemas reais.",
        "como_resolver": "1. Vá até a linha indicada.\n"
        "2. Troque 'except:' por 'except Exception:'.\n"
        "3. Se souber o erro exato, use-o (ex.: except ValueError:).",
        "como_confirmar": "Rode: ruff check .  O aviso E722 deve sumir.",
        "se_nao_funcionou": "Se o programa passou a parar com um erro que antes "
        "era escondido, isso é bom: agora o problema real apareceu.",
    },
    "E711": {
        "o_que_aconteceu": "Uma comparação com None usa '==' ou '!='.",
        "por_que": "A forma correta em Python é usar 'is' e 'is not'.",
        "como_resolver": "1. Vá até a linha indicada.\n"
        "2. Troque '== None' por 'is None'.\n"
        "3. Troque '!= None' por 'is not None'.",
        "como_confirmar": "Rode: ruff check .  O aviso E711 deve sumir.",
        "se_nao_funcionou": "Rode os testes (pytest) para garantir que o "
        "comportamento não mudou.",
    },
    "E712": {
        "o_que_aconteceu": "Uma comparação com True ou False usa '=='.",
        "por_que": "Comparar com True/False é redundante e pode dar resultados inesperados.",
        "como_resolver": "1. Vá até a linha indicada.\n"
        "2. Troque 'if x == True:' por 'if x:'.\n"
        "3. Troque 'if x == False:' por 'if not x:'.",
        "como_confirmar": "Rode: ruff check .  O aviso E712 deve sumir.",
        "se_nao_funcionou": "Rode os testes (pytest) para garantir que o "
        "comportamento não mudou.",
    },
    "E402": {
        "o_que_aconteceu": "Há um import no meio do arquivo, e não no topo.",
        "por_que": "Por convenção, todos os imports ficam no início do arquivo, "
        "antes do restante do código.",
        "como_resolver": "1. Recorte a linha de import indicada.\n"
        "2. Cole no topo do arquivo, junto dos outros imports.",
        "como_confirmar": "Rode: ruff check .  O aviso E402 deve sumir.",
        "se_nao_funcionou": "Se o import só funciona depois de alguma configuração "
        "anterior, peça ajuda: pode ser um caso legítimo.",
    },
    "E741": {
        "o_que_aconteceu": "Uma variável tem um nome ambíguo (l, O ou I).",
        "por_que": "Essas letras se confundem com os números 1 e 0 e dificultam a leitura.",
        "como_resolver": "1. Escolha um nome descritivo (ex.: 'linha' em vez de 'l').\n"
        "2. Troque o nome em todos os lugares onde a variável aparece "
        "(no VS Code: clique no nome e aperte F2).",
        "como_confirmar": "Rode: ruff check .  O aviso E741 deve sumir.",
        "se_nao_funcionou": "Use o F2 do VS Code em vez de trocar à mão: "
        "ele renomeia todas as ocorrências de uma vez.",
    },

    "I001": {
        "o_que_aconteceu": "Os imports do arquivo não estão na ordem padrão.",
        "por_que": "Por convenção, os imports ficam em grupos: primeiro os do "
        "Python, depois os de bibliotecas instaladas, depois os do próprio "
        "projeto, cada grupo separado por uma linha em branco.",
        "como_resolver": "1. No terminal, digite: ruff check --fix .\n"
        "2. O ruff reorganiza os imports sozinho.\n"
        "Se preferir fazer à mão: reordene as linhas de import seguindo os grupos acima.",
        "como_confirmar": "Rode: ruff check .  O aviso I001 deve sumir.",
        "se_nao_funcionou": "Se o ruff não mudou nada, confirme que salvou o arquivo "
        "(Ctrl+S) e que está na pasta do projeto.",
    },
}


def extrair_codigo(mensagem: str) -> str | None:
    achado = _CODIGO.match(mensagem)
    return achado.group(1) if achado else None


def buscar_no_catalogo(mensagem: str) -> dict | None:
    playbook = CATALOGO.get(extrair_codigo(mensagem))
    return dict(playbook) if playbook else None