"""Cria as tabelas do banco de dados.

Uso:
    python criar_banco.py             cria as tabelas que ainda não existem
    python criar_banco.py --exemplo   cria as tabelas e insere dados de exemplo (demonstração e testes)
    python criar_banco.py --recriar   APAGA TODOS OS DADOS e recria as tabelas vazias

Usuário de exemplo: demo@estoquefacil.com / senha demo123
"""
import sys
from datetime import timedelta
from decimal import Decimal

from sqlalchemy import select, text

from app import create_app
from app.extensions import db
from app.models import Categoria, Fornecedor, Produto, Usuario
from app.models.base import agora

# (código, nome, categoria, fornecedor, custo, venda, mínimo, entradas, saídas)
PRODUTOS_EXEMPLO = [
    ("7891000100", "Arroz Tipo 1 5kg", "Alimentos", "Distribuidora Sul Ltda.", "21.50", "27.90", 10, 40, 8),
    ("7891000200", "Café Torrado 500g", "Alimentos", "Atacadão Bom Preço", "13.90", "18.50", 10, 12, 10),
    ("7891000300", "Refrigerante 2L", "Bebidas", "Bebidas Paraná", "6.80", "9.99", 12, 48, 0),
    ("7891000400", "Detergente 500ml", "Limpeza", "Atacadão Bom Preço", "1.90", "2.79", 12, 17, 12),
    ("7891000500", "Feijão Carioca 1kg", "Alimentos", "Distribuidora Sul Ltda.", "6.20", "8.49", 10, 30, 3),
    ("7891000600", "Leite Integral 1L", "Bebidas", "Atacadão Bom Preço", "4.10", "5.99", 24, 36, 28),
    ("7891000700", "Água Mineral 500ml", "Bebidas", "Bebidas Paraná", "0.90", "2.00", 24, 60, 12),
    ("7891000800", "Sabão em Pó 1kg", "Limpeza", "Atacadão Bom Preço", "9.50", "13.90", 6, 15, 4),
    ("7891000900", "Papel Higiênico 12 rolos", "Higiene", "Distribuidora Sul Ltda.", "14.00", "19.90", 8, 20, 6),
    ("7891001000", "Creme Dental 90g", "Higiene", None, "3.20", "4.99", 10, 25, 7),
]


def inserir_dados_exemplo():
    if db.session.scalar(select(Usuario.id).limit(1)):
        print("O banco já tem dados; os dados de exemplo não foram inseridos.")
        return

    usuario = Usuario(nome="Usuário Demonstração", email="demo@estoquefacil.com")
    usuario.definir_senha("demo123")
    db.session.add(usuario)

    categorias = {
        nome: Categoria(nome=nome, descricao=descricao)
        for nome, descricao in [
            ("Alimentos", "Mercearia em geral"),
            ("Bebidas", "Bebidas e laticínios"),
            ("Limpeza", "Produtos de limpeza"),
            ("Higiene", "Higiene pessoal"),
        ]
    }
    fornecedores = {
        f.nome: f
        for f in [
            Fornecedor(nome="Distribuidora Sul Ltda.", cnpj="12345678000190", telefone="(41) 3333-1000", email="vendas@distsul.com.br"),
            Fornecedor(nome="Atacadão Bom Preço", cnpj="98765432000110", telefone="(41) 3333-2000"),
            Fornecedor(nome="Bebidas Paraná", telefone="(41) 99999-3000"),
        ]
    }
    db.session.add_all([*categorias.values(), *fornecedores.values()])

    for posicao, dados in enumerate(PRODUTOS_EXEMPLO, start=1):
        codigo, nome, categoria, fornecedor, custo, venda, minimo, entradas, saidas = dados
        produto = Produto(
            codigo=codigo,
            nome=nome,
            categoria=categorias[categoria],
            fornecedor=fornecedores.get(fornecedor),
            preco_custo=Decimal(custo),
            preco_venda=Decimal(venda),
            estoque_minimo=minimo,
        )
        db.session.add(produto)
        entrada = produto.registrar_entrada(entradas, usuario, "Estoque inicial")
        entrada.data_hora = agora() - timedelta(days=3)
        if saidas:
            saida = produto.registrar_saida(saidas, usuario, "Venda balcão")
            saida.data_hora = agora() - timedelta(hours=posicao * 5)  # espalha as vendas pelos últimos dias

    db.session.commit()
    print("Dados de exemplo inseridos. Login: demo@estoquefacil.com / senha: demo123")


def main():
    app = create_app()
    with app.app_context():
        if db.engine.url.get_backend_name() == "mysql":
            # Garante acentos corretos (ex.: "Café") nas tabelas criadas a seguir
            with db.engine.begin() as conexao:
                conexao.execute(text(
                    f"ALTER DATABASE `{db.engine.url.database}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
                ))
        if "--recriar" in sys.argv:
            db.drop_all()
            print("Tabelas apagadas.")
        db.create_all()
        url = db.engine.url
        local = url.database if url.get_backend_name() == "sqlite" else url.render_as_string(hide_password=True)
        print(f"Tabelas prontas em: {local}")
        if "--exemplo" in sys.argv:
            inserir_dados_exemplo()


if __name__ == "__main__":
    main()
