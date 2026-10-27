"""Configurações do EstoqueFácil.

Localmente o sistema usa SQLite (arquivo instance/estoque.db, sem instalar nada).
Em produção (PythonAnywhere) as variáveis de ambiente DATABASE_URL e SECRET_KEY
apontam para o MySQL e definem a chave secreta.
"""
import os


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
