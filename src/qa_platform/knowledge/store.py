import sqlite3

SCHEMA = """
CREATE TABLE IF NOT EXISTS bugs (
    fingerprint   TEXT PRIMARY KEY,
    modulo        TEXT NOT NULL,
    mensagem      TEXT NOT NULL,
    stack         TEXT,
    ocorrencias   INTEGER NOT NULL DEFAULT 1,
    primeira_vez  TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ultima_vez    TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS playbooks (
    fingerprint      TEXT PRIMARY KEY REFERENCES bugs(fingerprint),
    o_que_aconteceu  TEXT NOT NULL,
    por_que          TEXT NOT NULL,
    como_resolver    TEXT NOT NULL,
    como_confirmar   TEXT NOT NULL,
    se_nao_funcionou TEXT NOT NULL
);
"""

CAMPOS_PLAYBOOK = (
    "o_que_aconteceu",
    "por_que",
    "como_resolver",
    "como_confirmar",
    "se_nao_funcionou",
)


class Store:
    def __init__(self, caminho: str = "knowledge.db"):
        self.con = sqlite3.connect(caminho)
        self.con.row_factory = sqlite3.Row
        self.con.execute("PRAGMA foreign_keys = ON")
        self.con.executescript(SCHEMA)

    def registrar_bug(self, fingerprint, modulo, mensagem, stack=None) -> bool:
        """Registra um bug. Retorna True se ele já tinha acontecido antes."""
        existe = self.con.execute(
            "SELECT 1 FROM bugs WHERE fingerprint = ?", (fingerprint,)
        ).fetchone()
        if existe:
            self.con.execute(
                "UPDATE bugs SET ocorrencias = ocorrencias + 1, "
                "ultima_vez = CURRENT_TIMESTAMP WHERE fingerprint = ?",
                (fingerprint,),
            )
        else:
            self.con.execute(
                "INSERT INTO bugs (fingerprint, modulo, mensagem, stack) "
                "VALUES (?, ?, ?, ?)",
                (fingerprint, modulo, mensagem, stack),
            )
        self.con.commit()
        return existe is not None

    def buscar_bug(self, fingerprint):
        linha = self.con.execute(
            "SELECT * FROM bugs WHERE fingerprint = ?", (fingerprint,)
        ).fetchone()
        return dict(linha) if linha else None

    def salvar_playbook(self, fingerprint, **campos):
        faltando = [c for c in CAMPOS_PLAYBOOK if not campos.get(c)]
        if faltando:
            raise ValueError(f"Campos obrigatórios faltando: {faltando}")
        self.con.execute(
            "INSERT OR REPLACE INTO playbooks "
            "(fingerprint, o_que_aconteceu, por_que, como_resolver, "
            "como_confirmar, se_nao_funcionou) VALUES (?, ?, ?, ?, ?, ?)",
            (fingerprint, *(campos[c] for c in CAMPOS_PLAYBOOK)),
        )
        self.con.commit()

    def buscar_playbook(self, fingerprint):
        linha = self.con.execute(
            "SELECT * FROM playbooks WHERE fingerprint = ?", (fingerprint,)
        ).fetchone()
        return dict(linha) if linha else None

    def fechar(self):
        self.con.close()