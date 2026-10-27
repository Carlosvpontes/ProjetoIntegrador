"""Criação da aplicação Flask (padrão "application factory")."""
import os
import sqlite3

from flask import Flask, flash, redirect, render_template, request
from flask_wtf.csrf import CSRFError
from sqlalchemy import event
from sqlalchemy.engine import Engine

from app.extensions import csrf, db, login_manager
from app.formatacao import formatar_cnpj, formatar_data_hora, formatar_decimal, formatar_moeda
from config import Config


@event.listens_for(Engine, "connect")
def _ativar_chaves_estrangeiras_sqlite(conexao, _registro):
    """O SQLite só respeita chaves estrangeiras (RN06/RN07) com esta opção ligada."""
    if isinstance(conexao, sqlite3.Connection):
        cursor = conexao.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()


def create_app(config_class=Config):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_class)

    os.makedirs(app.instance_path, exist_ok=True)
    if not app.config.get("SQLALCHEMY_DATABASE_URI"):
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(app.instance_path, "estoque.db")
    if app.config["SQLALCHEMY_DATABASE_URI"].startswith("mysql"):
        # O MySQL do PythonAnywhere encerra conexões paradas há mais de 300 segundos
        app.config.setdefault("SQLALCHEMY_ENGINE_OPTIONS", {"pool_recycle": 280, "pool_pre_ping": True})

    db.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Faça login para acessar esta página."  # M33
    login_manager.login_message_category = "warning"

    from app.models import Usuario

    @login_manager.user_loader
    def carregar_usuario(usuario_id):
        return db.session.get(Usuario, int(usuario_id))

    from app.controllers import auth, categorias, fornecedores, movimentacoes, painel, produtos

    for modulo in (auth, painel, categorias, fornecedores, produtos, movimentacoes):
        app.register_blueprint(modulo.bp)

    app.jinja_env.filters["moeda"] = formatar_moeda
    app.jinja_env.filters["decimal"] = formatar_decimal
    app.jinja_env.filters["data_hora"] = formatar_data_hora
    app.jinja_env.filters["cnpj"] = formatar_cnpj

    @app.errorhandler(404)
    def pagina_nao_encontrada(_erro):
        return render_template("erros/404.html"), 404

    @app.errorhandler(500)
    def erro_interno(_erro):
        db.session.rollback()
        return render_template("erros/500.html"), 500

    @app.errorhandler(CSRFError)
    def sessao_expirada(_erro):
        flash("Sua sessão expirou. Tente novamente.", "warning")
        return redirect(request.path)

    return app
