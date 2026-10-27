"""Criar conta, entrar e sair (RF01, RF02)."""
from urllib.parse import urlsplit

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from sqlalchemy import select

from app.controllers.formularios import EMAIL_VALIDO
from app.extensions import db
from app.models import Usuario

bp = Blueprint("auth", __name__)

TAMANHO_MINIMO_SENHA = 6  # RN08


def _destino_seguro(destino):
    """Aceita apenas endereços internos do sistema, evitando redirecionar para outro site."""
    if not destino or not destino.startswith("/") or destino.startswith(("//", "/\\")):
        return None
    return destino if not urlsplit(destino).netloc else None


@bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("painel.index"))

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        senha = request.form.get("senha", "")
        usuario = db.session.scalar(select(Usuario).filter_by(email=email))

        if usuario and usuario.verificar_senha(senha):
            login_user(usuario)
            flash(f"Bem-vindo(a), {usuario.nome}!", "success")  # M02
            return redirect(_destino_seguro(request.args.get("next")) or url_for("painel.index"))

        flash("E-mail ou senha incorretos.", "danger")  # M22

    return render_template("auth/login.html", form=request.form)


@bp.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if current_user.is_authenticated:
        return redirect(url_for("painel.index"))

    erros = {}
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        email = request.form.get("email", "").strip().lower()
        senha = request.form.get("senha", "")
        confirmacao = request.form.get("confirmacao", "")

        if len(nome) < 2:
            erros["nome"] = "Informe seu nome (mínimo de 2 letras)."
        elif len(nome) > 100:
            erros["nome"] = "O nome pode ter no máximo 100 caracteres."

        if not EMAIL_VALIDO.match(email) or len(email) > 120:
            erros["email"] = "Informe um e-mail válido."
        elif db.session.scalar(select(Usuario.id).filter_by(email=email)):
            erros["email"] = "Este e-mail já está cadastrado."  # M23

        if len(senha) < TAMANHO_MINIMO_SENHA:
            erros["senha"] = "A senha deve ter no mínimo 6 caracteres."  # M24
        elif senha != confirmacao:
            erros["confirmacao"] = "As senhas não conferem."  # M25

        if not erros:
            usuario = Usuario(nome=nome, email=email)
            usuario.definir_senha(senha)
            db.session.add(usuario)
            db.session.commit()
            flash("Conta criada com sucesso! Faça login para continuar.", "success")  # M01
            return redirect(url_for("auth.login"))

        flash("Corrija os campos destacados.", "danger")

    return render_template("auth/cadastro.html", form=request.form, erros=erros)


@bp.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    flash("Você saiu do sistema.", "success")  # M03
    return redirect(url_for("auth.login"))
