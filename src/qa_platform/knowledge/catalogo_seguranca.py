import re

_CODIGO = re.compile(r"^(B\d{3}):")
_PACOTE = re.compile(r"^Dependência vulnerável: (\S+)")

_SENHA = {
    "o_que_aconteceu": "Uma senha, chave ou token está escrito direto no código.",
    "por_que": "Quem tiver acesso ao código (ou ao repositório no GitHub) vê o segredo. "
    "Mesmo apagando depois, ele continua no histórico do Git.",
    "como_resolver": "1. Troque o valor escrito no código por uma leitura de variável de "
    "ambiente: os.environ[\"NOME\"] (adicione 'import os' no topo).\n"
    "2. Defina a variável no seu computador ou no serviço onde o programa roda.\n"
    "3. Se o segredo já foi enviado ao GitHub, TROQUE a senha ou chave no serviço de "
    "origem: ela deve ser considerada vazada.",
    "como_confirmar": "Rode a análise de novo. O aviso deve sumir e o segredo não deve "
    "mais aparecer no código.",
    "se_nao_funcionou": "Se for só um texto de exemplo (não um segredo de verdade), "
    "pode ignorar o aviso. Mas nunca use senhas reais em exemplos.",
}

_EVAL = {
    "o_que_aconteceu": "O código usa eval() ou exec(), que executa texto como se fosse código.",
    "por_que": "Se esse texto vier de um usuário ou de fora, alguém pode fazer o "
    "programa executar qualquer coisa.",
    "como_resolver": "1. Vá até a linha indicada.\n"
    "2. Se o objetivo é converter texto em número, lista ou dicionário, use "
    "ast.literal_eval(texto) (com 'import ast' no topo), que só aceita valores simples.\n"
    "3. Se o objetivo é outro, procure uma alternativa sem eval/exec.",
    "como_confirmar": "Rode a análise de novo. O aviso deve sumir e o programa deve "
    "se comportar igual.",
    "se_nao_funcionou": "Se o texto é sempre escrito por você mesmo, o risco é baixo, "
    "mas ainda assim vale trocar.",
}

_PICKLE = {
    "o_que_aconteceu": "O código usa pickle, que carrega objetos salvos em arquivo.",
    "por_que": "Carregar um arquivo pickle de origem desconhecida pode executar "
    "código malicioso.",
    "como_resolver": "1. Se os dados são simples (textos, números, listas), troque por "
    "JSON: json.dump e json.load.\n"
    "2. Se precisa mesmo do pickle, carregue apenas arquivos criados pelo seu próprio "
    "programa, nunca arquivos baixados ou enviados por outras pessoas.",
    "como_confirmar": "Rode a análise de novo. O aviso deve sumir.",
    "se_nao_funcionou": "Se os dados têm objetos complexos, peça ajuda a quem "
    "desenvolve para escolher um formato seguro.",
}

_RANDOM = {
    "o_que_aconteceu": "O código usa o módulo random para gerar valores.",
    "por_que": "O random é previsível. Para senhas, códigos de verificação ou tokens, "
    "alguém pode adivinhar o próximo valor.",
    "como_resolver": "1. Se o valor é sensível (senha, token, código de confirmação), "
    "use o módulo secrets (import secrets), por exemplo: secrets.token_hex(16).\n"
    "2. Se é só para jogo, sorteio sem importância ou testes, o random está bem e "
    "o aviso pode ser ignorado.",
    "como_confirmar": "Rode a análise de novo. O aviso deve sumir (se você trocou "
    "por secrets).",
    "se_nao_funcionou": "Na dúvida se o valor é sensível, trate como sensível.",
}

_HASH = {
    "o_que_aconteceu": "Foi usado um algoritmo de hash fraco (MD5 ou SHA1).",
    "por_que": "Esses algoritmos já foram quebrados: não servem para proteger senhas "
    "nem para garantir a integridade de dados sensíveis.",
    "como_resolver": "1. Para guardar senhas, use bcrypt ou argon2 (bibliotecas feitas "
    "para isso), nunca um hash simples.\n"
    "2. Para outros casos, troque hashlib.md5 ou hashlib.sha1 por hashlib.sha256.\n"
    "3. Se o uso é só para identificar arquivos, sem fins de segurança, pode manter e "
    "adicionar usedforsecurity=False na chamada.",
    "como_confirmar": "Rode a análise de novo. O aviso deve sumir.",
    "se_nao_funcionou": "Se já existem senhas guardadas com o hash antigo, peça ajuda "
    "a quem desenvolve para migrá-las com segurança.",
}

_TLS = {
    "o_que_aconteceu": "O código desliga a verificação do certificado (verify=False) "
    "em uma conexão.",
    "por_que": "Sem a verificação, qualquer pessoa no caminho pode se passar pelo "
    "servidor e ler ou alterar os dados.",
    "como_resolver": "1. Apague o verify=False da chamada (o padrão já é verificar).\n"
    "2. Se der erro de certificado, o problema real está no certificado do servidor: "
    "peça a quem o administra para corrigi-lo, em vez de desligar a proteção.",
    "como_confirmar": "Rode a análise de novo. O aviso deve sumir e a conexão deve "
    "continuar funcionando.",
    "se_nao_funcionou": "Se o servidor usa um certificado próprio da empresa, aponte "
    "para ele: verify=\"caminho/do/certificado.pem\".",
}

_YAML = {
    "o_que_aconteceu": "O código usa yaml.load, que pode executar código escondido "
    "no arquivo.",
    "por_que": "Um arquivo YAML de origem desconhecida pode fazer o programa executar "
    "comandos.",
    "como_resolver": "Troque yaml.load(...) por yaml.safe_load(...).",
    "como_confirmar": "Rode a análise de novo. O aviso deve sumir e o arquivo deve "
    "continuar sendo lido normalmente.",
    "se_nao_funcionou": "Se o arquivo usa recursos avançados que o safe_load não "
    "aceita, peça ajuda a quem desenvolve.",
}

_SQL = {
    "o_que_aconteceu": "Um comando de banco de dados está sendo montado juntando textos.",
    "por_que": "Se um dos textos vier de um usuário, ele pode inserir comandos próprios "
    "(SQL injection) e ler ou apagar dados.",
    "como_resolver": "1. Não monte o comando com f-string, + ou %.\n"
    "2. Use parâmetros: cursor.execute(\"SELECT * FROM usuarios WHERE id = ?\", (id,)). "
    "O símbolo do parâmetro varia: ? no SQLite, %s no PostgreSQL e no MySQL.\n"
    "3. Nunca coloque o valor direto dentro do texto do comando.",
    "como_confirmar": "Rode a análise de novo. O aviso deve sumir e as consultas devem "
    "devolver os mesmos resultados.",
    "se_nao_funcionou": "Nomes de tabelas e colunas não aceitam parâmetros. Nesse caso, "
    "aceite só valores de uma lista fixa que você definiu.",
}

_SHELL = {
    "o_que_aconteceu": "O código executa um comando passando por um shell "
    "(shell=True ou os.system).",
    "por_que": "Se qualquer parte do comando vier de fora, alguém pode acrescentar "
    "comandos próprios.",
    "como_resolver": "1. Use subprocess.run com uma lista de partes, sem shell=True. "
    "Em vez de subprocess.run(\"ls \" + pasta, shell=True), use "
    "subprocess.run([\"ls\", pasta]).\n"
    "2. Troque os.system(...) por subprocess.run([...]).",
    "como_confirmar": "Rode a análise de novo. O aviso deve sumir e o comando deve "
    "continuar funcionando.",
    "se_nao_funcionou": "Se o comando usa recursos do shell (como | ou >), faça essa "
    "parte no próprio Python em vez de no comando.",
}

_SUBPROCESS = {
    "o_que_aconteceu": "O código executa outro programa (subprocess).",
    "por_que": "Executar programas só é arriscado quando parte do comando vem de fora "
    "(digitada por um usuário, de um arquivo ou de um site).",
    "como_resolver": "1. Confira se o comando é todo escrito por você, sem juntar "
    "textos vindos de fora.\n"
    "2. Passe o comando como lista de partes, sem shell=True.\n"
    "3. Quando possível, use o caminho completo do programa.",
    "como_confirmar": "Se o comando é fixo e confiável, este aviso pode ser ignorado.",
    "se_nao_funcionou": "Se parte do comando vem de fora, valide esse valor antes de "
    "usá-lo, aceitando apenas o que você espera.",
}

_BIND = {
    "o_que_aconteceu": "O servidor aceita conexões de qualquer computador da rede "
    "(endereço 0.0.0.0).",
    "por_que": "Em um computador pessoal, isso expõe o programa a outras pessoas "
    "da mesma rede.",
    "como_resolver": "1. Para uso local, troque \"0.0.0.0\" por \"127.0.0.1\".\n"
    "2. Se o programa precisa ser acessado de fora (em um servidor ou no Docker), "
    "mantenha 0.0.0.0, mas use firewall e exija login.",
    "como_confirmar": "Rode a análise de novo. O aviso deve sumir (se você usou 127.0.0.1).",
    "se_nao_funcionou": "Se, depois da troca, outro computador não consegue mais "
    "acessar o programa, é porque ele realmente precisava ficar aberto.",
}

_EXCEPT_PASS = {
    "o_que_aconteceu": "Um erro é capturado e simplesmente ignorado (except ... pass).",
    "por_que": "O programa continua como se nada tivesse acontecido, e o problema "
    "real fica escondido.",
    "como_resolver": "1. Vá até a linha indicada.\n"
    "2. Troque o 'pass' por um registro do erro: adicione 'import logging' no topo e "
    "use logging.exception(\"o que estava sendo feito\").\n"
    "3. Se o erro é esperado, capture só esse tipo (ex.: except FileNotFoundError:) "
    "em vez de qualquer erro.",
    "como_confirmar": "Rode a análise de novo. O aviso deve sumir.",
    "se_nao_funcionou": "Se o erro é esperado e inofensivo, escreva um comentário "
    "explicando o motivo e capture apenas o tipo específico.",
}

_TIMEOUT = {
    "o_que_aconteceu": "Uma requisição de rede não tem tempo limite.",
    "por_que": "Se o servidor não responder, o programa fica esperando para sempre.",
    "como_resolver": "Adicione timeout à chamada, por exemplo: requests.get(url, timeout=10).",
    "como_confirmar": "Rode a análise de novo. O aviso deve sumir.",
    "se_nao_funcionou": "Se a resposta costuma demorar mais, aumente o número "
    "(em segundos), mas nunca deixe sem limite.",
}

_DEBUG = {
    "o_que_aconteceu": "O Flask está com o modo de depuração ligado (debug=True).",
    "por_que": "Em um site no ar, esse modo permite que qualquer visitante execute "
    "código no servidor.",
    "como_resolver": "1. Use debug=True somente no seu computador.\n"
    "2. Em produção, remova o debug=True (ou leia o valor de uma variável de ambiente).",
    "como_confirmar": "Rode a análise de novo. O aviso deve sumir.",
    "se_nao_funcionou": "Confira se não há outro app.run(debug=True) em outro arquivo.",
}

CATALOGO_SEGURANCA = {
    "B105": _SENHA, "B106": _SENHA, "B107": _SENHA,
    "B102": _EVAL, "B307": _EVAL,
    "B301": _PICKLE, "B403": _PICKLE,
    "B311": _RANDOM,
    "B324": _HASH,
    "B501": _TLS,
    "B506": _YAML,
    "B608": _SQL,
    "B602": _SHELL, "B605": _SHELL,
    "B404": _SUBPROCESS, "B603": _SUBPROCESS, "B607": _SUBPROCESS,
    "B104": _BIND,
    "B110": _EXCEPT_PASS, "B112": _EXCEPT_PASS,
    "B113": _TIMEOUT,
    "B201": _DEBUG,
}

CATALOGO_PREFIXOS = {
    "Dependência vulnerável": {
        "o_que_aconteceu": "Uma biblioteca usada pelo projeto tem uma falha de "
        "segurança conhecida.",
        "por_que": "Falhas descobertas depois do lançamento são publicadas em bancos "
        "públicos de vulnerabilidades. Quem usa a versão antiga fica exposto.",
        "como_resolver": "1. Veja na mensagem a versão em que a falha foi corrigida.\n"
        "2. No terminal, com o ambiente virtual ativo, digite: "
        "pip install --upgrade {pacote}\n"
        "3. Atualize o número da versão no arquivo requirements.txt.\n"
        "4. Rode os testes do projeto (pytest) para garantir que nada quebrou.",
        "como_confirmar": "Rode a análise de novo. A biblioteca não deve mais aparecer.",
        "se_nao_funcionou": "Se a atualização quebrar o projeto, suba só até a menor "
        "versão corrigida. Se não existe versão corrigida, procure uma biblioteca "
        "alternativa.",
    },
    "Não foi possível verificar as dependências": {
        "o_que_aconteceu": "A ferramenta não conseguiu consultar o banco de falhas "
        "conhecidas.",
        "por_que": "Pode faltar internet, a ferramenta pip-audit pode não estar "
        "instalada, ou o requirements.txt tem algo que ela não entendeu.",
        "como_resolver": "1. Confira sua conexão com a internet.\n"
        "2. Instale a ferramenta: pip install pip-audit\n"
        "3. Confira se o requirements.txt tem um pacote por linha, no formato "
        "nome==versão.",
        "como_confirmar": "Rode a análise de novo. A verificação deve concluir.",
        "se_nao_funcionou": "Se aparecer um erro de rede, tente de novo mais tarde "
        "ou em outra conexão.",
    },
}


def buscar_no_catalogo_seguranca(mensagem: str) -> dict | None:
    for prefixo, playbook in CATALOGO_PREFIXOS.items():
        if mensagem.startswith(prefixo):
            achado = _PACOTE.match(mensagem)
            pacote = achado.group(1) if achado else "NOME_DO_PACOTE"
            return {c: t.replace("{pacote}", pacote) for c, t in playbook.items()}
    achado = _CODIGO.match(mensagem)
    playbook = CATALOGO_SEGURANCA.get(achado.group(1)) if achado else None
    return dict(playbook) if playbook else None