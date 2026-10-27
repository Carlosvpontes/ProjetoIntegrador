"""Gera o arquivo .env de produção: conexão com o MySQL do PythonAnywhere e chave secreta.

Uso (no console Bash do PythonAnywhere, dentro da pasta do projeto):
    python configurar_producao.py

O script pede a senha do MySQL (definida na aba "Databases"), testa a conexão
e só então grava o .env. A chave secreta é gerada automaticamente.
"""
import getpass
import secrets
import sys

from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL

from config import PASTA_PROJETO

USUARIO_PADRAO = "carlosvpontes"
NOME_BANCO = "estoque"


def montar_url(usuario, senha, nome_banco=NOME_BANCO):
    """URL de conexão do MySQL do PythonAnywhere. Caracteres especiais da senha são tratados aqui."""
    return URL.create(
        "mysql+pymysql",
        username=usuario,
        password=senha,
        host=f"{usuario}.mysql.pythonanywhere-services.com",
        database=f"{usuario}${nome_banco}",
        query={"charset": "utf8mb4"},
    )


def testar_conexao(url):
    motor = create_engine(url)
    try:
        with motor.connect() as conexao:
            conexao.execute(text("SELECT 1"))
    finally:
        motor.dispose()


def main():
    arquivo_env = PASTA_PROJETO / ".env"
    if arquivo_env.exists():
        resposta = input("O arquivo .env já existe. Substituir? (s/N): ").strip().lower()
        if resposta != "s":
            print("Nada foi alterado.")
            return

    usuario = input(f"Usuário do PythonAnywhere [{USUARIO_PADRAO}]: ").strip() or USUARIO_PADRAO
    senha = getpass.getpass("Senha do MySQL (não aparece enquanto você digita): ")
    url = montar_url(usuario, senha)

    print(f"Testando conexão com o banco {url.database} ...")
    try:
        testar_conexao(url)
    except Exception as erro:  # mostra o motivo ao usuário em vez de um traceback
        print("\n*** Não foi possível conectar ao MySQL. ***")
        print(f"Motivo: {erro.__class__.__name__}: {erro}")
        print(f'Confira a senha e se o banco "{NOME_BANCO}" foi criado na aba Databases.')
        sys.exit(1)

    arquivo_env.write_text(
        "# Configuração de produção, gerada por configurar_producao.py. NÃO publicar.\n"
        f"DATABASE_URL={url.render_as_string(hide_password=False)}\n"
        f"SECRET_KEY={secrets.token_hex(32)}\n",
        encoding="utf-8",
    )
    arquivo_env.chmod(0o600)  # apenas o dono do arquivo pode ler
    print("Conexão OK! Arquivo .env criado.")
    print("Próximo passo: python criar_banco.py --exemplo")


if __name__ == "__main__":
    main()
