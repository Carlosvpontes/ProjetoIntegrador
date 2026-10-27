import enum

from app.extensions import db
from app.models.base import agora
from app.models.erros import QuantidadeInvalidaError


class TipoMovimentacao(enum.Enum):
    ENTRADA = "Entrada"
    SAIDA = "Saída"


def validar_quantidade(valor):
    """RN02: aceita apenas número inteiro maior que zero (ex.: 5 ou "5").

    Retorna a quantidade como int ou lança QuantidadeInvalidaError.
    """
    texto = str(valor).strip()
    if not texto.isdecimal() or int(texto) <= 0:
        raise QuantidadeInvalidaError()
    return int(texto)


class Movimentacao(db.Model):
    """Entrada ou saída de mercadoria. É imutável depois de criada (RN11)."""

    __tablename__ = "movimentacao"
    __table_args__ = (
        db.CheckConstraint("quantidade > 0", name="ck_movimentacao_quantidade"),  # RN02
        db.Index("idx_mov_produto_data", "produto_id", "data_hora"),
        db.Index("idx_mov_data", "data_hora"),
    )

    id = db.Column(db.Integer, primary_key=True)
    produto_id = db.Column(db.Integer, db.ForeignKey("produto.id", ondelete="RESTRICT"), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuario.id", ondelete="RESTRICT"), nullable=False)
    tipo = db.Column(db.Enum(TipoMovimentacao, name="tipo_movimentacao"), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    observacao = db.Column(db.String(255))
    data_hora = db.Column(db.DateTime, nullable=False, default=agora)  # RN10

    produto = db.relationship("Produto", back_populates="movimentacoes")
    usuario = db.relationship("Usuario", back_populates="movimentacoes")

    def __repr__(self):
        return f"<Movimentacao {self.tipo.name} {self.quantidade}x produto={self.produto_id}>"
