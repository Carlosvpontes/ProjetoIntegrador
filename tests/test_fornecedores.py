"""Testes do cadastro de fornecedores (RF04, RN06)."""
import html

from sqlalchemy import select

from app.extensions import db
from app.models import Fornecedor


def _texto(resposta):
    """HTML da resposta com as entidades convertidas (&#34; vira "), como o navegador exibe."""
    return html.unescape(resposta.get_data(as_text=True))


def _dados(**alteracoes):
    dados = {"nome": "Atacadão Bom Preço", "cnpj": "98.765.432/0001-10", "telefone": "(41) 3333-2000", "email": "Vendas@Atacadao.com"}
    dados.update(alteracoes)
    return dados


def test_lista_exige_login(client):
    assert client.get("/fornecedores/").status_code == 302


def test_incluir_fornecedor_guarda_cnpj_somente_com_digitos(cliente_logado):
    resposta = cliente_logado.post("/fornecedores/novo", data=_dados(), follow_redirects=True)
    texto = _texto(resposta)
    assert "Fornecedor cadastrado com sucesso." in texto  # M04
    assert "98.765.432/0001-10" in texto  # exibido formatado na lista

    fornecedor = db.session.scalar(select(Fornecedor))
    assert fornecedor.cnpj == "98765432000110"
    assert fornecedor.email == "vendas@atacadao.com"


def test_incluir_somente_com_nome(cliente_logado):
    resposta = cliente_logado.post("/fornecedores/novo", data={"nome": "Bebidas Paraná"}, follow_redirects=True)
    assert "Fornecedor cadastrado com sucesso." in _texto(resposta)
    fornecedor = db.session.scalar(select(Fornecedor))
    assert fornecedor.cnpj is None
    assert fornecedor.telefone is None
    assert fornecedor.email is None


def test_cnpj_incompleto(cliente_logado):
    resposta = cliente_logado.post("/fornecedores/novo", data=_dados(cnpj="123"), follow_redirects=True)
    assert "CNPJ inválido: informe os 14 números." in _texto(resposta)  # M31


def test_cnpj_repetido(cliente_logado, fornecedor):
    resposta = cliente_logado.post("/fornecedores/novo", data=_dados(cnpj="12.345.678/0001-90"), follow_redirects=True)
    assert "Já existe um fornecedor com este CNPJ." in _texto(resposta)


def test_email_invalido(cliente_logado):
    resposta = cliente_logado.post("/fornecedores/novo", data=_dados(email="sem-arroba"), follow_redirects=True)
    assert "Informe um e-mail válido." in _texto(resposta)


def test_editar_fornecedor(cliente_logado, fornecedor):
    resposta = cliente_logado.post(
        f"/fornecedores/{fornecedor.id}/editar",
        data={"nome": "Distribuidora Sul Ltda.", "cnpj": fornecedor.cnpj},
        follow_redirects=True,
    )
    assert "Fornecedor atualizado com sucesso." in _texto(resposta)  # M05
    assert fornecedor.nome == "Distribuidora Sul Ltda."


def test_excluir_fornecedor_sem_produtos(cliente_logado, fornecedor):
    resposta = cliente_logado.post(f"/fornecedores/{fornecedor.id}/excluir", follow_redirects=True)
    assert "excluído com sucesso." in _texto(resposta)
    assert db.session.scalar(select(Fornecedor)) is None


def test_nao_exclui_fornecedor_com_produtos(cliente_logado, fornecedor, produto):
    produto.fornecedor = fornecedor
    db.session.commit()

    resposta = cliente_logado.post(f"/fornecedores/{fornecedor.id}/excluir", follow_redirects=True)
    assert "Não é possível excluir: existem 1 produto(s) vinculado(s)." in _texto(resposta)  # RN06
    assert db.session.get(Fornecedor, fornecedor.id) is not None
