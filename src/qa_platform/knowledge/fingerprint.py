import hashlib
import re


def normalizar(mensagem: str) -> str:
    texto = mensagem.lower()
    texto = re.sub(r"0x[0-9a-f]+", "<hex>", texto)
    texto = re.sub(r"[a-z]:\\[^\s]+|/[^\s]+", "<caminho>", texto)
    texto = re.sub(r"\d+", "<n>", texto)
    return re.sub(r"\s+", " ", texto).strip()


def gerar_fingerprint(modulo: str, mensagem: str) -> str:
    base = f"{modulo}|{normalizar(mensagem)}"
    return hashlib.sha256(base.encode()).hexdigest()[:16]