"""Testes da configuração de produção (.env e URL do MySQL)."""
import os

from sqlalchemy.engine import make_url

from config import carregar_env
from configurar_producao import montar_url


def test_url_do_mysql_do_pythonanywhere():
    url = montar_url("carlosvpontes", "segredo")
    assert url.drivername == "mysql+pymysql"
    assert url.host == "carlosvpontes.mysql.pythonanywhere-services.com"
    assert url.database == "carlosvpontes$estoque"
    assert url.query["charset"] == "utf8mb4"


def test_senha_com_caracteres_especiais_sobrevive_ao_arquivo_env():
    senha = "p@ss:w/rd#100%"
    texto = montar_url("carlosvpontes", senha).render_as_string(hide_password=False)
    lida = make_url(texto)
    assert lida.password == senha
    assert lida.database == "carlosvpontes$estoque"


def test_carregar_env(tmp_path, monkeypatch):
    monkeypatch.delenv("TESTE_VARIAVEL", raising=False)
    monkeypatch.delenv("TESTE_COM_IGUAL", raising=False)
    arquivo = tmp_path / ".env"
    arquivo.write_text("# comentário\nTESTE_VARIAVEL=abc\nTESTE_COM_IGUAL=a=b\n\n", encoding="utf-8")

    carregar_env(arquivo)

    assert os.environ["TESTE_VARIAVEL"] == "abc"
    assert os.environ["TESTE_COM_IGUAL"] == "a=b"


def test_carregar_env_nao_sobrescreve_variavel_existente(tmp_path, monkeypatch):
    monkeypatch.setenv("TESTE_VARIAVEL", "original")
    arquivo = tmp_path / ".env"
    arquivo.write_text("TESTE_VARIAVEL=novo\n", encoding="utf-8")

    carregar_env(arquivo)

    assert os.environ["TESTE_VARIAVEL"] == "original"


def test_arquivo_env_inexistente_e_ignorado(tmp_path):
    carregar_env(tmp_path / "nao-existe.env")  # não deve gerar erro
