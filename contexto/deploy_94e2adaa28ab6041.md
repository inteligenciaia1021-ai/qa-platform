# Erro 94e2adaa28ab6041

```
Container roda como administrador (root)
```

- **Módulo:** deploy
- **Ocorrências:** 1
- **Primeira vez:** 2026-11-23 01:34:05
- **Última vez:** 2026-11-23 01:34:05

## Guia de solução

### O que aconteceu

O programa dentro do container roda como administrador (root).

### Por que acontece

Se alguém explorar uma falha do programa, passa a ter controle total do container. Rodar com um usuário comum limita o estrago.

### Como resolver

1. No último estágio do Dockerfile, antes do CMD, crie um usuário comum e passe a usá-lo:  
   RUN useradd --create-home app  
   USER app  
2. Em imagens Alpine, use: RUN adduser -D app  
3. Se o programa precisa gravar arquivos, dê permissão a esse usuário na pasta onde ele grava.

### Como confirmar que resolveu

Rode a análise de novo. O aviso deve sumir e o programa deve continuar funcionando no container.

### Se não funcionou

Se aparecer erro de permissão, ele indica qual pasta o usuário comum não consegue acessar. Ajuste com COPY --chown=app ou chown.
