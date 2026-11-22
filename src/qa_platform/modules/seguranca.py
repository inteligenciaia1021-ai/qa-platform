import json
import subprocess
import sys
from pathlib import Path

from packaging.version import InvalidVersion, Version

from qa_platform.modules.base import Falha

NOME = "security"
_SENHAS = {"B105", "B106", "B107"}
_EXCLUIR = "*/.venv,*/.venv/*,*/node_modules,*/node_modules/*"


def _ler_bandit(texto: str) -> list[Falha]:
    try:
        dados = json.loads(texto or "{}")
    except json.JSONDecodeError as erro:
        raise RuntimeError(f"bandit devolveu algo inesperado: {erro}") from erro
    falhas = []
    for achado in dados.get("results", []):
        descricao = achado["issue_text"]
        if achado["test_id"] in _SENHAS:
            # não guarda o segredo em si na memória de bugs
            descricao = descricao.split(":")[0]
        mensagem = (
            f"{achado['test_id']}: {descricao} "
            f"[gravidade {achado['issue_severity']}]"
        )
        falhas.append(Falha(NOME, mensagem, achado["filename"], achado["line_number"]))
    return falhas


def _menor_correcao(versoes: list[str]) -> str | None:
    validas = []
    for texto in versoes:
        try:
            validas.append((Version(texto), texto))
        except InvalidVersion:
            continue
    return min(validas)[1] if validas else None


def _ler_pip_audit(texto: str, arquivo: str) -> list[Falha]:
    dados = json.loads(texto or "{}")
    falhas = []
    for dep in dados.get("dependencies", []):
        # o mesmo ID pode vir repetido: guarda um só
        vulns = {v["id"]: v for v in dep.get("vulns", [])}
        if not vulns:
            continue
        correcoes = [_menor_correcao(v.get("fix_versions") or []) for v in vulns.values()]
        com_correcao = [c for c in correcoes if c]
        base = f"Dependência vulnerável: {dep['name']} {dep.get('version', '?')}"
        total = f"{len(vulns)} falhas conhecidas"
        if com_correcao:
            alvo = max(com_correcao, key=Version)
            mensagem = f"{base} - atualizar para {alvo} ou superior ({total})"
        else:
            mensagem = f"{base} - sem versão corrigida disponível ({total})"
        falhas.append(Falha(NOME, mensagem, arquivo))
    return falhas


def _rodar_bandit(caminho: str) -> list[Falha]:
    resultado = subprocess.run(
        [
            sys.executable, "-m", "bandit", "-r", caminho,
            "-f", "json", "-q", "-s", "B101", "-x", _EXCLUIR,
        ],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    # B101 (uso de assert) é ignorado: em testes, assert é o normal.
    # Sem saída = a ferramenta nem rodou (ex.: não instalada). Não pode virar "tudo limpo".
    if resultado.returncode not in (0, 1) or not resultado.stdout.strip():
        raise RuntimeError(f"bandit falhou: {resultado.stderr.strip()}")
    return _ler_bandit(resultado.stdout)


def _rodar_pip_audit(caminho: str) -> list[Falha]:
    requisitos = Path(caminho) / "requirements.txt"
    if not requisitos.is_file():
        return []
    resultado = subprocess.run(
        [
            sys.executable, "-m", "pip_audit", "-r", str(requisitos),
            "-f", "json", "--progress-spinner", "off",
        ],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    if resultado.returncode not in (0, 1) or not resultado.stdout.strip():
        linhas = resultado.stderr.strip().splitlines()
        motivo = linhas[-1] if linhas else "motivo desconhecido"
        mensagem = f"Não foi possível verificar as dependências: {motivo}"
        return [Falha(NOME, mensagem, str(requisitos))]
    return _ler_pip_audit(resultado.stdout, str(requisitos))


class Seguranca:
    nome = NOME

    def rodar(self, caminho: str) -> list[Falha]:
        return _rodar_bandit(caminho) + _rodar_pip_audit(caminho)