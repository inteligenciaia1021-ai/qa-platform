from dataclasses import dataclass
from typing import Protocol


@dataclass
class Falha:
    modulo: str
    mensagem: str
    arquivo: str | None = None
    linha: int | None = None


class Modulo(Protocol):
    nome: str

    def rodar(self, caminho: str) -> list[Falha]: ...