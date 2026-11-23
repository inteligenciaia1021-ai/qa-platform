# Erro dbcea6828f27a55c

```
Segredo escrito no Dockerfile: variável API_TOKEN
```

- **Módulo:** deploy
- **Ocorrências:** 1
- **Primeira vez:** 2026-11-23 01:34:05
- **Última vez:** 2026-11-23 01:34:05

## Guia de solução

### O que aconteceu

Uma senha, chave ou token está escrito direto no Dockerfile.

### Por que acontece

Qualquer pessoa com acesso ao arquivo, ao repositório ou à imagem consegue ver o valor, mesmo que você o apague depois.

### Como resolver

1. Apague o valor do Dockerfile.  
2. Entregue o segredo só na hora de rodar o container, por exemplo: docker run -e NOME_DA_VARIAVEL=valor ... (ou com um arquivo .env que NÃO vai para o Git).  
3. Se o segredo já foi enviado ao GitHub ou a uma imagem publicada, TROQUE a senha ou a chave no serviço de origem: ela deve ser considerada vazada.

### Como confirmar que resolveu

Rode a análise de novo. O aviso deve sumir.

### Se não funcionou

Se o segredo é necessário durante a construção da imagem, use 'RUN --mount=type=secret' (BuildKit) em vez de ENV ou ARG.
