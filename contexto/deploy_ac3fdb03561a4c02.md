# Erro ac3fdb03561a4c02

```
Download executado direto no shell (curl | sh)
```

- **Módulo:** deploy
- **Ocorrências:** 1
- **Primeira vez:** 2026-11-23 01:34:05
- **Última vez:** 2026-11-23 01:34:05

## Guia de solução

### O que aconteceu

O Dockerfile baixa um script da internet e o executa imediatamente (curl ... | sh).

### Por que acontece

Você executa um código sem saber o que há nele. Se o site for invadido ou o endereço mudar, o seu build executa código de outra pessoa.

### Como resolver

1. Baixe o arquivo para dentro do projeto e leia o que ele faz.  
2. Prefira instalar o programa pelo gerenciador de pacotes (apt, pip, npm).  
3. Se precisa mesmo baixar, confira a integridade com um hash (sha256sum) antes de executar.

### Como confirmar que resolveu

Rode a análise de novo. O aviso deve sumir.

### Se não funcionou

Se o instalador oficial só existe nesse formato, fixe a versão no endereço e verifique o hash publicado pelo fabricante.
