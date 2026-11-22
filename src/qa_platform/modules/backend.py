import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

from qa_platform.modules.base import Falha


def _resumo(elemento: ET.Element) -> str:
    primeira = (elemento.get("message") or "").splitlines()
    texto = primeira[0] if primeira else "sem mensagem"
    # Erros de importação vêm só como "collection failure"; o motivo real
    # está no corpo, nas linhas que começam com "E ".
    if texto == "collection failure":
        linhas_e = [
            linha[1:].strip()
            for linha in (elemento.text or "").splitlines()
            if linha.startswith("E ")
        ]
        if linhas_e:
            texto = linhas_e[-1]
    return texto


def _nome_do_teste(caso: ET.Element) -> str:
    classe = caso.get("classname")
    nome = caso.get("name")
    return f"{classe}::{nome}" if classe else nome


class Backend:
    nome = "backend"

    def rodar(self, caminho: str) -> list[Falha]:
        with tempfile.TemporaryDirectory() as pasta:
            relatorio = Path(pasta) / "resultado.xml"
            resultado = subprocess.run(
                [
                    sys.executable, "-m", "pytest",
                    "--continue-on-collection-errors",
                    f"--junitxml={relatorio}", "-p", "no:cacheprovider", "-q",
                ],
                cwd=caminho,
                capture_output=True,
                text=True,
                check=False,
            )
            # código 5 = o pytest não encontrou nenhum teste
            if resultado.returncode == 5:
                return [Falha(self.nome, "Nenhum teste foi encontrado neste projeto")]
            if not relatorio.exists():
                detalhe = (resultado.stdout + resultado.stderr).strip()
                raise RuntimeError(f"pytest não gerou relatório: {detalhe}")
            return self._ler(relatorio)

    def _ler(self, relatorio: Path) -> list[Falha]:
        falhas = []
        for caso in ET.parse(relatorio).getroot().iter("testcase"):
            for filho in caso:
                if filho.tag in ("failure", "error"):
                    falhas.append(
                        Falha(
                            modulo=self.nome,
                            mensagem=_resumo(filho),
                            arquivo=_nome_do_teste(caso),
                        )
                    )
        return falhas