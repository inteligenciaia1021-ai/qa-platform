# Erro d85eac3bac916ecc

```
Dependência vulnerável: requests 2.19.0 - atualizar para 2.33.0 ou superior (5 falhas conhecidas)
```

- **Módulo:** security
- **Ocorrências:** 1
- **Primeira vez:** 2026-11-22 22:49:21
- **Última vez:** 2026-11-22 22:49:21

## Guia de solução

### O que aconteceu

Uma biblioteca usada pelo projeto tem uma falha de segurança conhecida.

### Por que acontece

Falhas descobertas depois do lançamento são publicadas em bancos públicos de vulnerabilidades. Quem usa a versão antiga fica exposto.

### Como resolver

1. Veja na mensagem a versão em que a falha foi corrigida.  
2. No terminal, com o ambiente virtual ativo, digite: pip install --upgrade requests  
3. Atualize o número da versão no arquivo requirements.txt.  
4. Rode os testes do projeto (pytest) para garantir que nada quebrou.

### Como confirmar que resolveu

Rode a análise de novo. A biblioteca não deve mais aparecer.

### Se não funcionou

Se a atualização quebrar o projeto, suba só até a menor versão corrigida. Se não existe versão corrigida, procure uma biblioteca alternativa.
