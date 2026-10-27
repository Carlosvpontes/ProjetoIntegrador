"""Cadastro de fornecedores (RF04, RN06)."""
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required
from sqlalchemy import select

from app.controllers.formularios import EMAIL_VALIDO, somente_digitos, texto
from app.extensions import db
from app.models import Fornecedor

bp = Blueprint("fornecedores", __name__, url_prefix="/fornecedores")


@bp.before_request
@login_required
def _exigir_login():
    """Todas as telas de fornecedores exigem login (RN09)."""


@bp.route("/")
def lista():
    fornecedores = db.session.scalars(select(Fornecedor).order_by(Fornecedor.nome)).all()
    return render_template("fornecedores/lista.html", fornecedores=fornecedores)


@bp.route("/novo", methods=["GET", "POST"])
def novo():
    return _formulario(Fornecedor())


@bp.route("/<int:id>/editar", methods=["GET", "POST"])
def editar(id):
    return _formulario(db.get_or_404(Fornecedor, id))


@bp.route("/<int:id>/excluir", methods=["POST"])
def excluir(id):
    fornecedor = db.get_or_404(Fornecedor, id)
    if not fornecedor.pode_excluir():  # RN06
        flash(f"Não é possível excluir: existem {len(fornecedor.produtos)} produto(s) vinculado(s).", "danger")  # M27
    else:
        db.session.delete(fornecedor)
        db.session.commit()
        flash(f'Fornecedor "{fornecedor.nome}" excluído com sucesso.', "success")  # M06
    return redirect(url_for(".lista"))


def _cnpj_em_uso(cnpj, ignorar_id):
    consulta = select(Fornecedor.id).where(Fornecedor.cnpj == cnpj)
    if ignorar_id:
        consulta = consulta.where(Fornecedor.id != ignorar_id)
    return db.session.scalar(consulta) is not None


def _formulario(fornecedor):
    novo = fornecedor.id is None
    erros = {}

    if request.method == "POST":
        form = request.form
        nome = texto(form, "nome")
        cnpj = somente_digitos(texto(form, "cnpj"))
        telefone = texto(form, "telefone")
        email = texto(form, "email").lower()

        if not 2 <= len(nome) <= 100:
            erros["nome"] = "Informe o nome do fornecedor (2 a 100 caracteres)."
        if cnpj and len(cnpj) != 14:
            erros["cnpj"] = "CNPJ inválido: informe os 14 números."  # M31
        elif cnpj and _cnpj_em_uso(cnpj, fornecedor.id):
            erros["cnpj"] = "Já existe um fornecedor com este CNPJ."
        if len(telefone) > 20:
            erros["telefone"] = "O telefone pode ter no máximo 20 caracteres."
        if email and (not EMAIL_VALIDO.match(email) or len(email) > 120):
            erros["email"] = "Informe um e-mail válido."

        if not erros:
            fornecedor.nome = nome
            fornecedor.cnpj = cnpj or None
            fornecedor.telefone = telefone or None
            fornecedor.email = email or None
            if novo:
                db.session.add(fornecedor)
            db.session.commit()
            flash(f"Fornecedor {'cadastrado' if novo else 'atualizado'} com sucesso.", "success")  # M04/M05
            return redirect(url_for(".lista"))

        flash("Corrija os campos destacados.", "danger")
    else:
        form = {
            "nome": fornecedor.nome or "",
            "cnpj": fornecedor.cnpj or "",
            "telefone": fornecedor.telefone or "",
            "email": fornecedor.email or "",
        }

    return render_template("fornecedores/form.html", fornecedor=fornecedor, novo=novo, form=form, erros=erros)
