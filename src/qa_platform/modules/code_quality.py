import json
import subprocess
import sys

from qa_platform.modules.base import Falha


class CodeQuality:
    nome = "code_quality"

    def rodar(self, caminho: str) -> list[Falha]:
        resultado = subprocess.run(
            [
                sys.executable, "-m", "ruff", "check",
                "--output-format", "json", "--no-cache", caminho,
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        # ruff retorna 0 (sem problemas) ou 1 (achou problemas); outro valor é falha real
        if resultado.returncode not in (0, 1):
            raise RuntimeError(f"ruff falhou: {resultado.stderr.strip()}")

        achados = json.loads(resultado.stdout or "[]")
        return [
            Falha(
                modulo=self.nome,
                mensagem=f"{a['code']}: {a['message']}",
                arquivo=a["filename"],
                linha=a["location"]["row"],
            )
            for a in achados
        ]