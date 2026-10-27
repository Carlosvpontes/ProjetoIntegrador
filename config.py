"""Configurações do EstoqueFácil.

Localmente o sistema usa SQLite (arquivo instance/estoque.db, sem instalar nada).
Em produção (PythonAnywhere) o arquivo .env, gerado por configurar_producao.py,
define DATABASE_URL (MySQL) e SECRET_KEY. O .env nunca vai para o GitHub.
"""
import os
from pathlib import Path

PASTA_PROJETO = Path(__file__).resolve().parent


def carregar_env(arquivo=PASTA_PROJETO / ".env"):
    """Lê linhas NOME=valor do arquivo .env para as variáveis de ambiente (sem sobrescrever as existentes)."""
    if not arquivo.exists():
        return
    for linha in arquivo.read_text(encoding="utf-8").splitlines():
        linha = linha.strip()
        if linha and not linha.startswith("#") and "=" in linha:
            nome, valor = linha.split("=", 1)
            os.environ.setdefault(nome.strip(), valor.strip())


carregar_env()


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "chave-local-de-desenvolvimento")
    # Quando vazio, app/__init__.py usa SQLite na pasta instance/
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestConfig(Config):
    TESTING = True
    SECRET_KEY = "chave-de-teste"
    SQLALCHEMY_DATABASE_URI = "sqlite://"  # banco em memória, apagado ao fim de cada teste
    WTF_CSRF_ENABLED = False
