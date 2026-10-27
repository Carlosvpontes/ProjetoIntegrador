"""Cadastro e pesquisa de produtos (RF05, RF10, RF11, RN03, RN05, RN07, RN12)."""
import re

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required
from sqlalchemy import func, or_, select

from app.controllers.formularios import ler_decimal, ler_inteiro_nao_negativo, padrao_busca, texto
from app.extensions import db
from app.formatacao import formatar_decimal
from app.models import Categoria, Fornecedor, Produto

bp = Blueprint("produtos", __name__, url_prefix="/produtos")

CODIGO_VALIDO = re.compile(r"^[A-Za-z0-9-]{1,30}$")


@bp.before_request
@login_required
def _exigir_login():
    """Todas as telas de produtos exigem login (RN09)."""


@bp.route("/")
def lista():
    busca = texto(request.args, "q")
    categoria_id = request.args.get("categoria", type=int)
    somente_baixo = request.args.get("situacao") == "baixo"

    consulta = select(Produto).order_by(Produto.nome)
    if busca:  # RF10
        padrao = padrao_busca(busca)
        consulta = consulta.where(or_(Produto.nome.ilike(padrao, escape="\\"), Produto.codigo.ilike(padrao, escape="\\")))
    if categoria_id:
        consulta = consulta.where(Produto.categoria_id == categoria_id)
    if somente_baixo:  # RF11 / RN04
        consulta = consulta.where(Produto.quantidade_atual <= Produto.estoque_minimo)

    return render_template(
        "produtos/lista.html",
        produtos=db.session.scalars(consulta).all(),
        categorias=_categorias(),
        filtros={"q": busca, "categoria": categoria_id, "situacao": "baixo" if somente_baixo else ""},
        filtrando=bool(busca or categoria_id or somente_baixo),
    )


@bp.route("/novo", methods=["GET", "POST"])
def novo():
    return _formulario(Produto())


@bp.route("/<int:id>/editar", methods=["GET", "POST"])
def editar(id):
    return _formulario(db.get_or_404(Produto, id))


@bp.route("/<int:id>/excluir", methods=["POST"])
def excluir(id):
    produto = db.get_or_404(Produto, id)
    if not produto.pode_excluir():  # RN07
        flash(  # M28
            "Não é possível excluir: este produto possui movimentações. "
            "Para corrigir o estoque, registre uma movimentação inversa.",
            "danger",
        )
    else:
        db.session.delete(produto)
        db.session.commit()
        flash(f'Produto "{produto.nome}" excluído com sucesso.', "success")  # M06
    return redirect(url_for(".lista"))


def _categorias():
    return db.session.scalars(select(Categoria).order_by(Categoria.nome)).all()


def _fornecedores():
    return db.session.scalars(select(Fornecedor).order_by(Fornecedor.nome)).all()


def _codigo_em_uso(codigo, ignorar_id):
    consulta = select(Produto.id).where(func.lower(Produto.codigo) == codigo.lower())
    if ignorar_id:
        consulta = consulta.where(Produto.id != ignorar_id)
    return db.session.scalar(consulta) is not None


def _ler_id(form, campo, modelo):
    """Converte o valor de uma lista de seleção no objeto correspondente (None se vazio ou inexistente)."""
    valor = texto(form, campo)
    return db.session.get(modelo, int(valor)) if valor.isdecimal() and len(valor) <= 9 else None


def _formulario(produto):
    novo = produto.id is None
    erros = {}

    if request.method == "POST":
        form = request.form
        codigo = texto(form, "codigo")
        nome = texto(form, "nome")
        descricao = texto(form, "descricao")
        categoria = _ler_id(form, "categoria_id", Categoria)
        fornecedor = _ler_id(form, "fornecedor_id", Fornecedor)

        if not CODIGO_VALIDO.match(codigo):
            erros["codigo"] = "Informe o código (até 30 letras, números ou hífen)."
        elif _codigo_em_uso(codigo, produto.id):
            erros["codigo"] = f'Já existe um produto com o código "{codigo}".'  # M26
        if not 2 <= len(nome) <= 100:
            erros["nome"] = "Informe o nome do produto (2 a 100 caracteres)."
        if len(descricao) > 255:
            erros["descricao"] = "A descrição pode ter no máximo 255 caracteres."
        if categoria is None:
            erros["categoria_id"] = "Selecione uma categoria."
        if texto(form, "fornecedor_id") and fornecedor is None:
            erros["fornecedor_id"] = "Fornecedor não encontrado."

        valores = {}
        for campo, leitor in [
            ("preco_custo", ler_decimal),
            ("preco_venda", ler_decimal),
            ("estoque_minimo", ler_inteiro_nao_negativo),
        ]:
            try:
                valores[campo] = leitor(form.get(campo))
            except ValueError as erro:
                erros[campo] = str(erro)  # M30 e validações numéricas (RN12)

        if not erros:
            produto.codigo = codigo
            produto.nome = nome
            produto.descricao = descricao or None
            produto.categoria = categoria
            produto.fornecedor = fornecedor
            produto.preco_custo = valores["preco_custo"]
            produto.preco_venda = valores["preco_venda"]
            produto.estoque_minimo = valores["estoque_minimo"]
            # quantidade_atual não vem do formulário: só muda por movimentações (RN03)
            if novo:
                db.session.add(produto)
            db.session.commit()
            flash(f"Produto {'cadastrado' if novo else 'atualizado'} com sucesso.", "success")  # M04/M05
            return redirect(url_for(".lista"))

        flash("Corrija os campos destacados.", "danger")
    else:
        form = {
            "codigo": produto.codigo or "",
            "nome": produto.nome or "",
            "descricao": produto.descricao or "",
            "categoria_id": str(produto.categoria_id or ""),
            "fornecedor_id": str(produto.fornecedor_id or ""),
            "preco_custo": formatar_decimal(produto.preco_custo),
            "preco_venda": formatar_decimal(produto.preco_venda),
            "estoque_minimo": str(produto.estoque_minimo),
        }

    return render_template(
        "produtos/form.html",
        produto=produto,
        novo=novo,
        form=form,
        erros=erros,
        opcoes_categorias=[(c.id, c.nome) for c in _categorias()],
        opcoes_fornecedores=[(f.id, f.nome) for f in _fornecedores()],
    )
