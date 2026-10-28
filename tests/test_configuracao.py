"""Testes da configuração de produção (connection string do Neon e arquivo .env)."""
import os

import pytest

from config import carregar_env, normalizar_url_banco

URL_NEON = "postgresql://neondb_owner:abc123@ep-cool-lab-a1b2c3.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
ESPERADO = "postgresql+psycopg://neondb_owner:abc123@ep-cool-lab-a1b2c3.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"


@pytest.mark.parametrize(
    "copiado",
    [
        URL_NEON,
        f"  {URL_NEON}  ",
        f"'{URL_NEON}'",
        f"psql '{URL_NEON}'",
        URL_NEON.replace("postgresql://", "postgres://"),
    ],
)
def test_connection_string_do_neon_e_convertida_para_o_driver_psycopg(copiado):
    assert normalizar_url_banco(copiado) == ESPERADO


def test_url_vazia_significa_usar_sqlite_local():
    assert normalizar_url_banco(None) is None
    assert normalizar_url_banco("") is None


def test_outras_urls_nao_sao_alteradas():
    assert normalizar_url_banco("sqlite:///estoque.db") == "sqlite:///estoque.db"


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
