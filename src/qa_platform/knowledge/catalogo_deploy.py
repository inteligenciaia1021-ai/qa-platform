CATALOGO_DEPLOY = {
    "Servidor não respondeu": {
        "o_que_aconteceu": "O endereço testado não devolveu nenhuma resposta.",
        "por_que": "O servidor pode estar desligado, o endereço pode estar errado, "
        "uma porta pode estar bloqueada ou a internet pode ter caído.",
        "como_resolver": "1. Confira o endereço: ele deve começar com http:// ou "
        "https:// e, se for local, ter a porta (ex.: :8000).\n"
        "2. Abra o mesmo endereço no navegador.\n"
        "3. Se o servidor é seu, confirme que o programa está rodando e leia o "
        "terminal dele.\n"
        "4. Em um servidor na nuvem, confira se a máquina está ligada e se o "
        "firewall libera a porta.",
        "como_confirmar": "Rode a análise de novo. O servidor deve responder.",
        "se_nao_funcionou": "Teste de outra rede (por exemplo, o celular) para saber "
        "se o problema é só na sua conexão.",
    },
    "Servidor respondeu com erro": {
        "o_que_aconteceu": "O servidor respondeu, mas com um código de erro (HTTP).",
        "por_que": "Códigos 5xx (500, 502, 503) indicam falha dentro do servidor. "
        "Código 404 indica que a página não existe naquele endereço. Códigos 401 "
        "e 403 indicam falta de login ou de permissão.",
        "como_resolver": "1. Veja o código na mensagem.\n"
        "2. Se começa com 5, abra o terminal ou os logs do servidor: o erro "
        "detalhado aparece lá. Corrija o problema indicado.\n"
        "3. Se é 404, confira se o endereço está certo e se o arquivo ou a rota "
        "existe.\n"
        "4. Se é 401 ou 403, confira o login ou a chave de acesso.",
        "como_confirmar": "Rode a análise de novo. O código deve ser 200.",
        "se_nao_funcionou": "Se o erro só acontece depois de publicar, compare as "
        "configurações do servidor com as do seu computador (variáveis de ambiente "
        "e banco de dados costumam ser a causa).",
    },
    "Resposta lenta": {
        "o_que_aconteceu": "O servidor respondeu, mas demorou mais do que o limite.",
        "por_que": "Pode ser servidor sobrecarregado, banco de dados lento, uma "
        "consulta pesada ou uma máquina pequena demais.",
        "como_resolver": "1. Rode a análise de novo para ver se foi algo pontual.\n"
        "2. Se a lentidão se repete, descubra qual parte demora (abra o F12 do "
        "navegador, aba 'Network').\n"
        "3. Peça a quem desenvolve para revisar as consultas ao banco e o uso de "
        "memória do servidor.",
        "como_confirmar": "Rode a análise de novo. O tempo deve ficar abaixo do limite.",
        "se_nao_funcionou": "Se o servidor 'acorda' devagar na primeira visita, "
        "pode ser um plano gratuito que hiberna quando fica parado.",
    },
    "Certificado inválido": {
        "o_que_aconteceu": "O certificado de segurança (HTTPS) do site não é aceito "
        "pelos navegadores.",
        "por_que": "O certificado pode estar vencido, ser feito para outro endereço "
        "ou ser autoassinado (criado pelo próprio dono, sem uma entidade confiável).",
        "como_resolver": "1. Veja o motivo na mensagem (ex.: 'certificate has "
        "expired', 'self-signed certificate').\n"
        "2. Se venceu, renove o certificado. Com Let's Encrypt (gratuito), "
        "geralmente basta rodar: certbot renew\n"
        "3. Se é para outro endereço, emita um certificado para o endereço correto.\n"
        "4. Se é autoassinado em um ambiente de testes, isso é esperado.",
        "como_confirmar": "Abra o site no navegador: não deve aparecer aviso de "
        "segurança. Rode a análise de novo.",
        "se_nao_funcionou": "Se usa hospedagem ou CDN, o certificado costuma ser "
        "renovado pelo painel do próprio serviço.",
    },
    "Certificado perto de vencer": {
        "o_que_aconteceu": "O certificado de segurança (HTTPS) do site vence em breve.",
        "por_que": "Certificados têm validade. Depois que vencem, os navegadores "
        "mostram um aviso assustador e muitos visitantes saem do site.",
        "como_resolver": "1. Renove o certificado antes da data.\n"
        "2. Com Let's Encrypt (gratuito): certbot renew\n"
        "3. Em hospedagens e CDNs, procure a opção de renovação no painel.\n"
        "4. Configure a renovação automática para não depender de lembrar.",
        "como_confirmar": "Rode a análise de novo. O aviso deve sumir.",
        "se_nao_funcionou": "Se a renovação automática já existe e falhou, confira "
        "os logs dela: o motivo costuma ser um domínio que mudou de lugar.",
    },
    "Imagem base sem versão fixa": {
        "o_que_aconteceu": "O Dockerfile parte de uma imagem sem versão definida "
        "(ou com a etiqueta 'latest').",
        "por_que": "'latest' muda com o tempo. O mesmo Dockerfile pode funcionar hoje "
        "e quebrar semana que vem, quando a imagem for atualizada.",
        "como_resolver": "1. Troque a linha FROM por uma versão específica, por "
        "exemplo: FROM python:3.12-slim (em vez de FROM python ou python:latest).\n"
        "2. Para ver as versões disponíveis, abra a página da imagem em "
        "hub.docker.com e use a aba Tags.\n"
        "3. Refaça a imagem (docker build) e rode os testes.",
        "como_confirmar": "Rode a análise de novo. O aviso deve sumir.",
        "se_nao_funcionou": "Se a versão que você usa hoje não é conhecida, rode "
        "'docker run IMAGEM python --version' (ajuste para a sua imagem) para descobri-la.",
    },
    "Container roda como administrador": {
        "o_que_aconteceu": "O programa dentro do container roda como administrador (root).",
        "por_que": "Se alguém explorar uma falha do programa, passa a ter controle "
        "total do container. Rodar com um usuário comum limita o estrago.",
        "como_resolver": "1. No último estágio do Dockerfile, antes do CMD, crie um "
        "usuário comum e passe a usá-lo:\n"
        "   RUN useradd --create-home app\n"
        "   USER app\n"
        "2. Em imagens Alpine, use: RUN adduser -D app\n"
        "3. Se o programa precisa gravar arquivos, dê permissão a esse usuário "
        "na pasta onde ele grava.",
        "como_confirmar": "Rode a análise de novo. O aviso deve sumir e o programa "
        "deve continuar funcionando no container.",
        "se_nao_funcionou": "Se aparecer erro de permissão, ele indica qual pasta "
        "o usuário comum não consegue acessar. Ajuste com COPY --chown=app ou chown.",
    },
    "ADD usado": {
        "o_que_aconteceu": "O Dockerfile usa ADD para copiar arquivos locais.",
        "por_que": "O ADD faz coisas extras e menos óbvias (baixa endereços da "
        "internet e descompacta arquivos). Para copiar arquivos comuns, o COPY é "
        "mais claro e mais seguro.",
        "como_resolver": "Troque a palavra ADD por COPY na linha indicada.",
        "como_confirmar": "Rode a análise de novo e refaça a imagem (docker build). "
        "O aviso deve sumir.",
        "se_nao_funcionou": "Se você precisa baixar algo de um endereço da internet, "
        "faça isso com RUN curl ... (e confira o arquivo baixado).",
    },
    "Segredo escrito no Dockerfile": {
        "o_que_aconteceu": "Uma senha, chave ou token está escrito direto no Dockerfile.",
        "por_que": "Qualquer pessoa com acesso ao arquivo, ao repositório ou à imagem "
        "consegue ver o valor, mesmo que você o apague depois.",
        "como_resolver": "1. Apague o valor do Dockerfile.\n"
        "2. Entregue o segredo só na hora de rodar o container, por exemplo: "
        "docker run -e NOME_DA_VARIAVEL=valor ... (ou com um arquivo .env que NÃO "
        "vai para o Git).\n"
        "3. Se o segredo já foi enviado ao GitHub ou a uma imagem publicada, "
        "TROQUE a senha ou a chave no serviço de origem: ela deve ser considerada vazada.",
        "como_confirmar": "Rode a análise de novo. O aviso deve sumir.",
        "se_nao_funcionou": "Se o segredo é necessário durante a construção da imagem, "
        "use 'RUN --mount=type=secret' (BuildKit) em vez de ENV ou ARG.",
    },
    "Download executado direto": {
        "o_que_aconteceu": "O Dockerfile baixa um script da internet e o executa "
        "imediatamente (curl ... | sh).",
        "por_que": "Você executa um código sem saber o que há nele. Se o site for "
        "invadido ou o endereço mudar, o seu build executa código de outra pessoa.",
        "como_resolver": "1. Baixe o arquivo para dentro do projeto e leia o que ele faz.\n"
        "2. Prefira instalar o programa pelo gerenciador de pacotes (apt, pip, npm).\n"
        "3. Se precisa mesmo baixar, confira a integridade com um hash (sha256sum) "
        "antes de executar.",
        "como_confirmar": "Rode a análise de novo. O aviso deve sumir.",
        "se_nao_funcionou": "Se o instalador oficial só existe nesse formato, "
        "fixe a versão no endereço e verifique o hash publicado pelo fabricante.",
    },
    "Nada para verificar": {
        "o_que_aconteceu": "Não havia nada que este módulo pudesse analisar no "
        "endereço ou na pasta informados.",
        "por_que": "O módulo de deploy analisa arquivos Dockerfile ou endereços de "
        "servidores. A pasta informada não tem nenhum Dockerfile.",
        "como_resolver": "1. Se o projeto usa Docker, confira se você apontou para a "
        "pasta certa (onde está o arquivo chamado Dockerfile).\n"
        "2. Se quer testar um servidor no ar, informe o endereço completo, por "
        "exemplo: https://meusite.com\n"
        "3. Se o projeto não usa Docker, este aviso pode ser ignorado.",
        "como_confirmar": "Rode a análise de novo com o alvo certo.",
        "se_nao_funcionou": "Dockerfiles com outro nome precisam se chamar "
        "Dockerfile.algo ou algo.Dockerfile para serem encontrados.",
    },
    "Alvo não encontrado": {
        "o_que_aconteceu": "O caminho ou endereço informado não existe.",
        "por_que": "O nome pode estar escrito errado, ou faltou o http:// ou https:// "
        "no início do endereço.",
        "como_resolver": "1. Se é um endereço de site, comece com http:// ou https://.\n"
        "2. Se é uma pasta ou arquivo, confira o nome e o caminho (use Tab para "
        "completar no terminal).",
        "como_confirmar": "Rode a análise de novo.",
        "se_nao_funcionou": "Use 'pwd' para ver em qual pasta você está e 'dir' para "
        "ver o que existe nela.",
    },
}


def buscar_no_catalogo_deploy(mensagem: str) -> dict | None:
    for prefixo, playbook in CATALOGO_DEPLOY.items():
        if mensagem.startswith(prefixo):
            return dict(playbook)
    return None