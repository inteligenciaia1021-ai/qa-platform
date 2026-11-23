# Erro 39d8bc6de13394bc

```
ADD usado onde COPY basta
```

- **Módulo:** deploy
- **Ocorrências:** 1
- **Primeira vez:** 2026-11-23 01:34:05
- **Última vez:** 2026-11-23 01:34:05

## Guia de solução

### O que aconteceu

O Dockerfile usa ADD para copiar arquivos locais.

### Por que acontece

O ADD faz coisas extras e menos óbvias (baixa endereços da internet e descompacta arquivos). Para copiar arquivos comuns, o COPY é mais claro e mais seguro.

### Como resolver

Troque a palavra ADD por COPY na linha indicada.

### Como confirmar que resolveu

Rode a análise de novo e refaça a imagem (docker build). O aviso deve sumir.

### Se não funcionou

Se você precisa baixar algo de um endereço da internet, faça isso com RUN curl ... (e confira o arquivo baixado).
