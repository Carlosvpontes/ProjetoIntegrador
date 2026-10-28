"""Configurações do EstoqueFácil.

- No seu computador: SQLite (arquivo instance/estoque.db), sem instalar nada.
- Em produção (Render): a variável DATABASE_URL aponta para o PostgreSQL do Neon e
  SECRET_KEY é gerada pelo próprio Render (ver render.yaml).

Opcional: um arquivo .env na raiz do projeto (fora do GitHub) com linhas NOME=valor
também define essas variáveis, por exemplo para usar o banco do Neon localmente.
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


def normalizar_url_banco(url):
    """Ajusta a "connection string" copiada do Neon para o formato do SQLAlchemy.

    Aceita 'postgresql://...', 'postgres://...' e também o texto copiado com aspas ou
    com o prefixo "psql". Retorna None quando a variável não foi definida.
    """
    if not url:
        return None
    url = url.strip()
    if url.startswith("psql "):
        url = url[len("psql "):].strip()
    url = url.strip("'\"")
    for prefixo in ("postgresql://", "postgres://"):
        if url.startswith(prefixo):
            return "postgresql+psycopg://" + url[len(prefixo):]
    return url


carregar_env()


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "chave-local-de-desenvolvimento")
    # Quando vazio, app/__init__.py usa SQLite na pasta instance/
    SQLALCHEMY_DATABASE_URI = normalizar_url_banco(os.environ.get("DATABASE_URL"))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # No Render o site é acessado só por HTTPS: o cookie de login nunca trafega sem criptografia
    SESSION_COOKIE_SECURE = os.environ.get("RENDER") == "true"


class TestConfig(Config):
    TESTING = True
    SECRET_KEY = "chave-de-teste"
    # Padrão: banco SQLite em memória. TEST_DATABASE_URL permite rodar os mesmos testes no PostgreSQL.
    SQLALCHEMY_DATABASE_URI = normalizar_url_banco(os.environ.get("TEST_DATABASE_URL")) or "sqlite://"
    SESSION_COOKIE_SECURE = False
    WTF_CSRF_ENABLED = False
