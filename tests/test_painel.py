"""Testes do painel (RF09) e das páginas de erro (T13)."""
from app.formatacao import formatar_moeda
from app.extensions import db


def _texto(resposta):
    return resposta.get_data(as_text=True)


def test_painel_vazio(cliente_logado):
    texto = _texto(cliente_logado.get("/"))
    assert "Produtos cadastrados" in texto
    assert "R$ 0,00" in texto
    assert "Nenhum produto precisa de reposição." in texto
    assert "Nenhum registro encontrado." in texto  # M51


def test_painel_mostra_totais_e_estoque_baixo(cliente_logado, produto, usuario):
    produto.registrar_entrada(3, usuario, "Compra")  # 3 <= mínimo 5: estoque baixo
    db.session.commit()

    texto = _texto(cliente_logado.get("/"))
    assert "R$ 60,00" in texto  # 3 x R$ 20,00
    assert "1 produto(s) com estoque baixo." in texto  # M50
    assert "Arroz 5kg" in texto
    assert "Entrada" in texto


def test_produto_acima_do_minimo_nao_aparece_no_alerta(cliente_logado, produto, usuario):
    produto.registrar_entrada(50, usuario)
    db.session.commit()

    texto = _texto(cliente_logado.get("/"))
    assert "com estoque baixo." not in texto
    assert "Nenhum produto precisa de reposição." in texto


def test_pagina_inexistente_mostra_erro_404(cliente_logado):
    resposta = cliente_logado.get("/pagina-que-nao-existe")
    assert resposta.status_code == 404
    assert "Página não encontrada." in _texto(resposta)  # M34


def test_formatar_moeda():
    assert formatar_moeda(1234.5) == "R$ 1.234,50"
    assert formatar_moeda(0) == "R$ 0,00"
    assert formatar_moeda(None) == "R$ 0,00"
