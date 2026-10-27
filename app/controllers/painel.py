"""Painel inicial com a situação geral do estoque (RF09)."""
from flask import Blueprint, render_template
from flask_login import login_required
from sqlalchemy import func, select

from app.extensions import db
from app.models import Movimentacao, Produto
from app.models.base import agora

bp = Blueprint("painel", __name__)

QTD_ULTIMAS_MOVIMENTACOES = 5


@bp.route("/")
@login_required
def index():
    inicio_do_dia = agora().replace(hour=0, minute=0, second=0, microsecond=0)

    total_produtos = db.session.scalar(select(func.count(Produto.id)))
    valor_estoque = db.session.scalar(
        select(func.coalesce(func.sum(Produto.quantidade_atual * Produto.preco_custo), 0))
    )
    estoque_baixo = db.session.scalars(  # RN04
        select(Produto)
        .where(Produto.quantidade_atual <= Produto.estoque_minimo)
        .order_by(Produto.quantidade_atual, Produto.nome)
    ).all()
    movimentacoes_hoje = db.session.scalar(
        select(func.count(Movimentacao.id)).where(Movimentacao.data_hora >= inicio_do_dia)
    )
    ultimas_movimentacoes = db.session.scalars(
        select(Movimentacao)
        .order_by(Movimentacao.data_hora.desc(), Movimentacao.id.desc())
        .limit(QTD_ULTIMAS_MOVIMENTACOES)
    ).all()

    return render_template(
        "painel/index.html",
        total_produtos=total_produtos,
        valor_estoque=valor_estoque,
        estoque_baixo=estoque_baixo,
        movimentacoes_hoje=movimentacoes_hoje,
        ultimas_movimentacoes=ultimas_movimentacoes,
    )
