from qa_platform.core.diagnostico import diagnosticar
from qa_platform.core.exportador import exportar
from qa_platform.knowledge.store import Store


def test_exporta_um_arquivo_por_erro_e_um_indice(tmp_path):
    store = Store(":memory:")
    diagnosticar(store, "code_quality", "F401: `os` imported but unused")
    diagnosticar(store, "backend", "Erro inventado sem guia")
    assert exportar(store, str(tmp_path)) == 2
    arquivos = {a.name for a in tmp_path.glob("*.md")}
    assert "INDEX.md" in arquivos
    assert len(arquivos) == 3
    store.fechar()


def test_documento_traz_o_passo_a_passo(tmp_path):
    store = Store(":memory:")
    d = diagnosticar(store, "code_quality", "F401: `os` imported but unused")
    exportar(store, str(tmp_path))
    texto = (tmp_path / f"code_quality_{d.fingerprint}.md").read_text(encoding="utf-8")
    assert "Como resolver" in texto
    assert "Apague essa linha de import" in texto
    store.fechar()


def test_erro_sem_guia_e_marcado(tmp_path):
    store = Store(":memory:")
    d = diagnosticar(store, "backend", "Erro inventado sem guia")
    exportar(store, str(tmp_path))
    texto = (tmp_path / f"backend_{d.fingerprint}.md").read_text(encoding="utf-8")
    assert "Ainda não existe guia" in texto
    store.fechar()


def test_indice_nao_quebra_com_colchetes_e_barras(tmp_path):
    store = Store(":memory:")
    diagnosticar(store, "backend", "falha [grave] a | b")
    exportar(store, str(tmp_path))
    indice = (tmp_path / "INDEX.md").read_text(encoding="utf-8")
    assert "\\[grave\\]" in indice
    assert "a \\| b" in indice
    store.fechar()