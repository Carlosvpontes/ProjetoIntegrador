"""Testes das regras de negócio na camada Model."""
from decimal import Decimal

import pytest
from sqlalchemy.exc import IntegrityError

from app.extensions import db
from app.models import (
    Categoria,
    EstoqueInsuficienteError,
    Fornecedor,
    Produto,
    QuantidadeInvalidaError,
    TipoMovimentacao,
    validar_quantidade,
)


# ---------- Usuário ----------

def test_senha_e_guardada_criptografada(usuario):
    assert usuario.senha_hash != "senha123"
    assert usuario.verificar_senha("senha123")
    assert not usuario.verificar_senha("senha-errada")


# ---------- RN02: quantidade válida ----------

@pytest.mark.parametrize("valor, esperado", [(1, 1), ("5", 5), (" 12 ", 12)])
def test_quantidade_valida(valor, esperado):
    assert validar_quantidade(valor) == esperado


@pytest.mark.parametrize("valor", [0, -3, "0", "-1", "2.5", "abc", "", None, 1.5])
def test_quantidade_invalida(valor):
    with pytest.raises(QuantidadeInvalidaError):
        validar_quantidade(valor)


# ---------- Entradas e saídas ----------

def test_produto_novo_comeca_com_estoque_zero(produto):
    assert produto.quantidade_atual == 0  # RN03


def test_produto_ainda_nao_salvo_aceita_entrada(categoria, usuario):
    produto = Produto(codigo="P900", nome="Novo", categoria=categoria)
    assert produto.quantidade_atual == 0
    produto.registrar_entrada(7, usuario)
    db.session.add(produto)
    db.session.commit()
    assert produto.quantidade_atual == 7


def test_entrada_soma_ao_estoque_e_registra_movimentacao(produto, usuario):
    mov = produto.registrar_entrada(10, usuario, "Compra")
    db.session.commit()

    assert produto.quantidade_atual == 10
    assert mov.tipo == TipoMovimentacao.ENTRADA
    assert mov.quantidade == 10
    assert mov.usuario == usuario  # RN10
    assert mov.data_hora is not None  # RN10
    assert produto.movimentacoes == [mov]


def test_saida_subtrai_do_estoque(produto, usuario):
    produto.registrar_entrada(10, usuario)
    mov = produto.registrar_saida(4, usuario)
    db.session.commit()

    assert produto.quantidade_atual == 6
    assert mov.tipo == TipoMovimentacao.SAIDA


def test_saida_pode_zerar_o_estoque(produto, usuario):
    produto.registrar_entrada(3, usuario)
    produto.registrar_saida(3, usuario)
    assert produto.quantidade_atual == 0


def test_saida_maior_que_estoque_e_bloqueada(produto, usuario):
    produto.registrar_entrada(2, usuario)
    db.session.commit()

    with pytest.raises(EstoqueInsuficienteError) as erro:  # RN01
        produto.registrar_saida(5, usuario)

    assert erro.value.disponivel == 2
    assert 'há apenas 2 unidade(s) de "Arroz 5kg"' in str(erro.value)
    assert produto.quantidade_atual == 2  # nada foi alterado
    assert len(produto.movimentacoes) == 1  # só a entrada


def test_movimentacao_com_quantidade_invalida_nao_altera_estoque(produto, usuario):
    with pytest.raises(QuantidadeInvalidaError):
        produto.registrar_entrada(0, usuario)
    assert produto.quantidade_atual == 0
    assert produto.movimentacoes == []


def test_observacao_vazia_vira_nula(produto, usuario):
    mov = produto.registrar_entrada(1, usuario, "   ")
    assert mov.observacao is None


# ---------- RN04: estoque baixo ----------

@pytest.mark.parametrize("quantidade, baixo", [(4, True), (5, True), (6, False)])
def test_estoque_baixo_quando_menor_ou_igual_ao_minimo(produto, usuario, quantidade, baixo):
    produto.registrar_entrada(quantidade, usuario)
    assert produto.estoque_baixo() is baixo


def test_valor_em_estoque(produto, usuario):
    produto.registrar_entrada(3, usuario)
    assert produto.valor_em_estoque() == Decimal("60.00")


# ---------- RN06 e RN07: exclusões ----------

def test_categoria_com_produtos_nao_pode_ser_excluida(categoria, produto):
    assert not categoria.pode_excluir()


def test_categoria_sem_produtos_pode_ser_excluida(categoria):
    assert categoria.pode_excluir()


def test_fornecedor_com_produtos_nao_pode_ser_excluido(produto):
    fornecedor = Fornecedor(nome="Distribuidora")
    produto.fornecedor = fornecedor
    db.session.commit()
    assert not fornecedor.pode_excluir()


def test_produto_com_movimentacoes_nao_pode_ser_excluido(produto, usuario):
    assert produto.pode_excluir()
    produto.registrar_entrada(1, usuario)
    db.session.commit()
    assert not produto.pode_excluir()


def test_banco_impede_excluir_categoria_com_produtos(categoria, produto):
    """Mesmo que o código falhe, o banco garante a RN06 (chave estrangeira RESTRICT)."""
    db.session.delete(categoria)
    with pytest.raises(IntegrityError):
        db.session.commit()
    db.session.rollback()


# ---------- Restrições de unicidade ----------

def test_codigo_de_produto_e_unico(categoria, produto):  # RN05
    db.session.add(Produto(codigo="P001", nome="Outro", categoria=categoria))
    with pytest.raises(IntegrityError):
        db.session.commit()
    db.session.rollback()


def test_nome_de_categoria_e_unico(categoria):
    db.session.add(Categoria(nome="Alimentos"))
    with pytest.raises(IntegrityError):
        db.session.commit()
    db.session.rollback()
