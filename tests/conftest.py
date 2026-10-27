"""Preparação comum dos testes: cada teste roda em um banco vazio, em memória."""
from decimal import Decimal

import pytest

from app import create_app
from app.extensions import db
from app.models import Categoria, Fornecedor, Produto, Usuario
from config import TestConfig

SENHA_PADRAO = "senha123"


@pytest.fixture
def app():
    app = create_app(TestConfig)
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def usuario(app):
    usuario = Usuario(nome="Márcia Teste", email="marcia@teste.com")
    usuario.definir_senha(SENHA_PADRAO)
    db.session.add(usuario)
    db.session.commit()
    return usuario


@pytest.fixture
def cliente_logado(client, usuario):
    client.post("/login", data={"email": usuario.email, "senha": SENHA_PADRAO})
    return client


@pytest.fixture
def categoria(app):
    categoria = Categoria(nome="Alimentos")
    db.session.add(categoria)
    db.session.commit()
    return categoria


@pytest.fixture
def fornecedor(app):
    fornecedor = Fornecedor(nome="Distribuidora Sul", cnpj="12345678000190")
    db.session.add(fornecedor)
    db.session.commit()
    return fornecedor


@pytest.fixture
def produto(categoria):
    """Produto com estoque zero e estoque mínimo 5."""
    produto = Produto(
        codigo="P001",
        nome="Arroz 5kg",
        categoria=categoria,
        preco_custo=Decimal("20.00"),
        preco_venda=Decimal("27.90"),
        estoque_minimo=5,
    )
    db.session.add(produto)
    db.session.commit()
    return produto
