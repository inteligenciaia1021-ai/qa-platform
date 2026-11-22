CATALOGO_FRONTEND = {
    "Erro de JavaScript": {
        "o_que_aconteceu": "O código da página (JavaScript) encontrou um erro e parou de funcionar naquele ponto.",
        "por_que": "Em geral, algo usado no código não existe (nome escrito errado ou "
        "arquivo que não carregou) ou um valor veio vazio quando não deveria.",
        "como_resolver": "1. Abra a página no navegador e aperte F12.\n"
        "2. Clique na aba 'Console': o erro aparece em vermelho, com o nome do arquivo e a linha.\n"
        "3. Vá até essa linha no código.\n"
        "4. Se a mensagem diz 'is not defined', o nome não existe: confira a escrita "
        "ou se o arquivo que o define está sendo carregado.",
        "como_confirmar": "Recarregue a página (Ctrl+F5) com o Console aberto. O erro vermelho deve sumir.",
        "se_nao_funcionou": "Corrija um erro por vez: um erro costuma esconder outros que só aparecem depois.",
    },
    "Recurso não encontrado": {
        "o_que_aconteceu": "A página pede um arquivo (imagem, estilo ou script) que não existe naquele endereço.",
        "por_que": "O arquivo foi apagado ou movido, ou o nome/caminho está escrito errado "
        "(maiúsculas e minúsculas contam).",
        "como_resolver": "1. Veja o endereço do arquivo na mensagem.\n"
        "2. Confira se o arquivo existe na pasta do projeto.\n"
        "3. Se existe, corrija o caminho no HTML ou CSS para ficar idêntico ao nome real.\n"
        "4. Se não existe, adicione o arquivo ou remova a referência a ele.",
        "como_confirmar": "Recarregue a página com F12 aberto, na aba 'Network'. Nenhuma linha deve ficar vermelha.",
        "se_nao_funcionou": "Confira se o arquivo foi salvo na pasta certa e se a extensão está correta (.png, .jpg, .css).",
    },
    "Erro do servidor": {
        "o_que_aconteceu": "O servidor respondeu com um erro interno ao receber o pedido da página.",
        "por_que": "O problema está no código do servidor (o back-end), não na página em si.",
        "como_resolver": "1. Veja o endereço que falhou na mensagem.\n"
        "2. Abra o terminal onde o servidor está rodando: o erro detalhado aparece lá.\n"
        "3. Use esse erro para corrigir o código do servidor.",
        "como_confirmar": "Recarregue a página. O pedido deve responder sem erro.",
        "se_nao_funcionou": "Se não houver mensagem no terminal, procure os arquivos de log do servidor.",
    },
    "Resposta com erro": {
        "o_que_aconteceu": "O servidor recusou um pedido da página.",
        "por_que": "Códigos 401 e 403 indicam falta de permissão ou de login. Outros "
        "códigos 4xx indicam um pedido que o servidor não aceita.",
        "como_resolver": "1. Veja o código de erro (HTTP ...) e o endereço na mensagem.\n"
        "2. Se for 401 ou 403, confira se o login ou a chave de acesso estão corretos.\n"
        "3. Nos demais casos, confira se o endereço e os dados enviados estão certos.",
        "como_confirmar": "Recarregue a página. O pedido deve funcionar.",
        "se_nao_funcionou": "Teste o mesmo endereço direto no navegador para ver a resposta completa.",
    },
    "Falha de rede": {
        "o_que_aconteceu": "A página tentou carregar algo e a conexão falhou ou foi bloqueada.",
        "por_que": "O servidor pode estar desligado, o endereço pode estar errado ou "
        "a conexão com a internet pode ter caído.",
        "como_resolver": "1. Confirme que o servidor está ligado.\n"
        "2. Confira o endereço na mensagem.\n"
        "3. Teste sua conexão com a internet.",
        "como_confirmar": "Recarregue a página. O arquivo deve carregar.",
        "se_nao_funcionou": "Se o endereço é de outro site, pode ser que ele bloqueie o acesso: use um arquivo próprio.",
    },
    "Página sem título": {
        "o_que_aconteceu": "A página não tem um título.",
        "por_que": "O título aparece na aba do navegador e nos resultados de busca. "
        "Sem ele, a página fica sem identificação.",
        "como_resolver": "1. Abra o arquivo HTML da página.\n"
        "2. Dentro de <head>, adicione: <title>Nome da sua página</title>",
        "como_confirmar": "Abra a página: o título deve aparecer na aba do navegador.",
        "se_nao_funcionou": "Confira se o <title> está dentro do <head> e se salvou o arquivo (Ctrl+S).",
    },
    "Imagem sem texto alternativo": {
        "o_que_aconteceu": "Uma imagem não tem descrição em texto.",
        "por_que": "Pessoas que usam leitores de tela não sabem o que a imagem mostra, "
        "e o texto aparece no lugar se a imagem não carregar.",
        "como_resolver": "1. Encontre a imagem no HTML (a tag <img>).\n"
        "2. Adicione o atributo alt com uma descrição curta, por exemplo: "
        '<img src="logo.png" alt="Logo da loja">\n'
        '3. Se a imagem é só decorativa, use alt vazio: alt=""',
        "como_confirmar": "Rode a análise de novo. O aviso deve sumir.",
        "se_nao_funcionou": "Confira se o alt está dentro da mesma tag <img>, antes do símbolo >.",
    },
    "Página não abriu": {
        "o_que_aconteceu": "O navegador de teste não conseguiu abrir o endereço informado.",
        "por_que": "O endereço pode estar errado, ou o servidor pode estar desligado.",
        "como_resolver": "1. Confira o endereço digitado (incluindo http:// ou https://).\n"
        "2. Abra o mesmo endereço no seu navegador para ver se carrega.\n"
        "3. Se for um servidor local, confirme que ele está rodando.",
        "como_confirmar": "Rode a análise de novo. A página deve abrir.",
        "se_nao_funcionou": "Se passou o caminho de uma pasta em vez de um endereço, confirme que a pasta existe.",
    },
}


def buscar_no_catalogo_frontend(mensagem: str) -> dict | None:
    for prefixo, playbook in CATALOGO_FRONTEND.items():
        if mensagem.startswith(prefixo):
            return dict(playbook)
    return None