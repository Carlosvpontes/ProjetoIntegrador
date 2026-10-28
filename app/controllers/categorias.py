"""Cadastro de categorias (RF03, RN06)."""
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required
from sqlalchemy import func, select

from app.controllers.formularios import texto
from app.extensions import db
from app.models import Categoria

bp = Blueprint("categorias", __name__, url_prefix="/categorias")


@bp.before_request
@login_required
def _exigir_login():
    """Todas as telas de categorias exigem login (RN09)."""


@bp.route("/")
def lista():
    categorias = db.session.scalars(select(Categoria).order_by(Categoria.nome)).all()
    return render_template("categorias/lista.html", categorias=categorias)


@bp.route("/nova", methods=["GET", "POST"])
def nova():
    return _formulario(Categoria())


@bp.route("/<int:id>/editar", methods=["GET", "POST"])
def editar(id):
    return _formulario(db.get_or_404(Categoria, id))


@bp.route("/<int:id>/excluir", methods=["POST"])
def excluir(id):
    categoria = db.get_or_404(Categoria, id)
    if not categoria.pode_excluir():  # RN06
        flash(f"Não é possível excluir: existem {len(categoria.produtos)} produto(s) vinculado(s).", "danger")  # M27
    else:
        db.session.delete(categoria)
        db.session.commit()
        flash(f'Categoria "{categoria.nome}" excluída com sucesso.', "success")  # M06
    return redirect(url_for(".lista"))


def _nome_em_uso(nome, ignorar_id):
    """Compara sem diferenciar maiúsculas: "Bebidas" e "bebidas" são o mesmo nome."""
    consulta = select(Categoria.id).where(func.lower(Categoria.nome) == nome.lower())
    if ignorar_id:
        consulta = consulta.where(Categoria.id != ignorar_id)
    return db.session.scalar(consulta) is not None


def _formulario(categoria):
    nova = categoria.id is None
    erros = {}

    if request.method == "POST":
        form = request.form
        nome = texto(form, "nome")
        descricao = texto(form, "descricao")

        if not 2 <= len(nome) <= 60:
            erros["nome"] = "Informe o nome da categoria (2 a 60 caracteres)."
        elif _nome_em_uso(nome, categoria.id):
            erros["nome"] = "Já existe uma categoria com esse nome."  # M32
        if len(descricao) > 255:
            erros["descricao"] = "A descrição pode ter no máximo 255 caracteres."

        if not erros:
            categoria.nome = nome
            categoria.descricao = descricao or None
            if nova:
                db.session.add(categoria)
            db.session.commit()
            flash(f"Categoria {'cadastrada' if nova else 'atualizada'} com sucesso.", "success")  # M04/M05
            return redirect(url_for(".lista"))

        flash("Corrija os campos destacados.", "danger")
    else:
        form = {"nome": categoria.nome or "", "descricao": categoria.descricao or ""}

    return render_template("categorias/form.html", categoria=categoria, nova=nova, form=form, erros=erros)
