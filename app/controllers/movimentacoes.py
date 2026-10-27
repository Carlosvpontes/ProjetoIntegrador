"""Entradas, saídas e histórico de movimentações (RF06, RF07, RF08, RN01, RN02, RN10, RN11).

Não existem rotas de edição ou exclusão: movimentações são imutáveis (RN11).
"""
from datetime import datetime, timedelta

from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from sqlalchemy import select

from app.controllers.formularios import texto
from app.extensions import db
from app.models import EstoqueInsuficienteError, Movimentacao, Produto, QuantidadeInvalidaError, TipoMovimentacao
from app.models.base import agora

bp = Blueprint("movimentacoes", __name__, url_prefix="/movimentacoes")

TIPOS_NA_URL = {"entrada": TipoMovimentacao.ENTRADA, "saida": TipoMovimentacao.SAIDA}
DIAS_PADRAO_HISTORICO = 30
LIMITE_HISTORICO = 500


@bp.before_request
@login_required
def _exigir_login():
    """Todas as telas de movimentações exigem login (RN09)."""


def _ler_data(valor):
    try:
        return datetime.strptime(valor, "%Y-%m-%d").date() if valor else None
    except ValueError:
        return None


@bp.route("/")
def historico():
    hoje = agora().date()
    filtros = {
        "produto": request.args.get("produto", type=int),
        "tipo": request.args.get("tipo", ""),
        # Sem filtro informado, mostra os últimos 30 dias (padrão pré-preenchido da IHC)
        "inicio": _ler_data(request.args.get("inicio")) if "inicio" in request.args else hoje - timedelta(days=DIAS_PADRAO_HISTORICO),
        "fim": _ler_data(request.args.get("fim")) if "fim" in request.args else hoje,
    }

    consulta = select(Movimentacao).order_by(Movimentacao.data_hora.desc(), Movimentacao.id.desc())
    if filtros["produto"]:
        consulta = consulta.where(Movimentacao.produto_id == filtros["produto"])
    if filtros["tipo"] in ("ENTRADA", "SAIDA"):
        consulta = consulta.where(Movimentacao.tipo == TipoMovimentacao[filtros["tipo"]])
    if filtros["inicio"]:
        consulta = consulta.where(Movimentacao.data_hora >= datetime.combine(filtros["inicio"], datetime.min.time()))
    if filtros["fim"]:  # inclui o dia final inteiro
        consulta = consulta.where(Movimentacao.data_hora < datetime.combine(filtros["fim"] + timedelta(days=1), datetime.min.time()))

    movimentacoes = db.session.scalars(consulta.limit(LIMITE_HISTORICO + 1)).all()
    return render_template(
        "movimentacoes/historico.html",
        movimentacoes=movimentacoes[:LIMITE_HISTORICO],
        limite_atingido=len(movimentacoes) > LIMITE_HISTORICO,
        limite=LIMITE_HISTORICO,
        filtros=filtros,
        produtos=_produtos(),
    )


@bp.route("/nova/<tipo>", methods=["GET", "POST"])
def nova(tipo):
    if tipo not in TIPOS_NA_URL:
        abort(404)
    tipo_movimentacao = TIPOS_NA_URL[tipo]
    erros = {}
    mensagem_erro = "Corrija os campos destacados."

    if request.method == "POST":
        form = request.form
        produto_id = texto(form, "produto_id")
        observacao = texto(form, "observacao")
        # Bloqueia a linha do produto até o fim da transação: duas saídas simultâneas
        # não conseguem, juntas, tirar mais do que existe (RN01). No SQLite é ignorado.
        produto = (
            db.session.get(Produto, int(produto_id), with_for_update=True)
            if produto_id.isdecimal() and len(produto_id) <= 9
            else None
        )

        if produto is None:
            erros["produto_id"] = "Selecione um produto."
        if len(observacao) > 255:
            erros["observacao"] = "A observação pode ter no máximo 255 caracteres."

        if not erros:
            try:
                if tipo_movimentacao is TipoMovimentacao.ENTRADA:
                    movimentacao = produto.registrar_entrada(form.get("quantidade"), current_user, observacao)
                else:
                    movimentacao = produto.registrar_saida(form.get("quantidade"), current_user, observacao)
            except QuantidadeInvalidaError as erro:  # RN02
                erros["quantidade"] = str(erro)  # M20
            except EstoqueInsuficienteError as erro:  # RN01
                erros["quantidade"] = f"Máximo disponível: {erro.disponivel}"
                mensagem_erro = str(erro)  # M21

        if not erros:
            db.session.commit()
            acao = "Entrada" if tipo_movimentacao is TipoMovimentacao.ENTRADA else "Saída"
            flash(f'{acao} de {movimentacao.quantidade} unidade(s) de "{produto.nome}" registrada.', "success")  # M10/M11
            if tipo_movimentacao is TipoMovimentacao.SAIDA and produto.estoque_baixo():
                flash(f'Atenção: "{produto.nome}" está com estoque baixo ({produto.quantidade_atual} unidade(s)).', "warning")  # M52
            return redirect(url_for(".historico"))

        db.session.rollback()  # libera o bloqueio do produto; nada foi alterado
        flash(mensagem_erro, "danger")
        return _tela_formulario(tipo, form, erros)

    form = {"produto_id": request.args.get("produto", "")}
    return _tela_formulario(tipo, form, erros)


def _produtos():
    return db.session.scalars(select(Produto).order_by(Produto.nome)).all()


def _tela_formulario(tipo, form, erros):
    produtos = _produtos()
    return render_template(
        "movimentacoes/form.html",
        tipo=tipo,
        entrada=tipo == "entrada",
        form=form,
        erros=erros,
        opcoes_produtos=[(p.id, f"{p.nome} — {p.codigo} (estoque: {p.quantidade_atual})") for p in produtos],
    )
