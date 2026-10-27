from decimal import Decimal

from app.extensions import db
from app.models.base import agora
from app.models.erros import EstoqueInsuficienteError
from app.models.movimentacao import Movimentacao, TipoMovimentacao, validar_quantidade


class Produto(db.Model):
    """Item controlado no estoque. Concentra as regras de entrada e saída."""

    __tablename__ = "produto"
    __table_args__ = (
        db.CheckConstraint("preco_custo >= 0", name="ck_produto_preco_custo"),  # RN12
        db.CheckConstraint("preco_venda >= 0", name="ck_produto_preco_venda"),  # RN12
        db.CheckConstraint("estoque_minimo >= 0", name="ck_produto_estoque_minimo"),
        db.CheckConstraint("quantidade_atual >= 0", name="ck_produto_quantidade_atual"),
        db.Index("idx_produto_nome", "nome"),  # RF10
    )

    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(30), nullable=False, unique=True)  # RN05
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(255))
    categoria_id = db.Column(db.Integer, db.ForeignKey("categoria.id", ondelete="RESTRICT"), nullable=False)
    fornecedor_id = db.Column(db.Integer, db.ForeignKey("fornecedor.id", ondelete="RESTRICT"))
    preco_custo = db.Column(db.Numeric(10, 2), nullable=False, default=Decimal("0.00"))
    preco_venda = db.Column(db.Numeric(10, 2), nullable=False, default=Decimal("0.00"))
    estoque_minimo = db.Column(db.Integer, nullable=False, default=0)
    # RN03: alterada somente por registrar_entrada/registrar_saida, nunca pelo formulário
    quantidade_atual = db.Column(db.Integer, nullable=False, default=0)
    criado_em = db.Column(db.DateTime, nullable=False, default=agora)
    atualizado_em = db.Column(db.DateTime, nullable=False, default=agora, onupdate=agora)

    categoria = db.relationship("Categoria", back_populates="produtos")
    fornecedor = db.relationship("Fornecedor", back_populates="produtos")
    movimentacoes = db.relationship(
        "Movimentacao",
        back_populates="produto",
        passive_deletes="all",
        order_by="Movimentacao.data_hora.desc()",
    )

    def __init__(self, **campos):
        # Os "default" das colunas só valem ao gravar no banco; aqui o produto
        # já nasce com estoque zero para permitir movimentações antes de salvar (RN03).
        campos.setdefault("quantidade_atual", 0)
        campos.setdefault("estoque_minimo", 0)
        campos.setdefault("preco_custo", Decimal("0.00"))
        campos.setdefault("preco_venda", Decimal("0.00"))
        super().__init__(**campos)

    def estoque_baixo(self):
        """RN04: estoque atual menor ou igual ao estoque mínimo."""
        return self.quantidade_atual <= self.estoque_minimo

    def valor_em_estoque(self):
        return Decimal(self.quantidade_atual) * Decimal(self.preco_custo)

    def pode_excluir(self):
        """RN07: produto com movimentações não pode ser excluído (preserva o histórico)."""
        return len(self.movimentacoes) == 0

    def registrar_entrada(self, quantidade, usuario, observacao=None):
        quantidade = validar_quantidade(quantidade)
        self.quantidade_atual += quantidade
        return self._nova_movimentacao(TipoMovimentacao.ENTRADA, quantidade, usuario, observacao)

    def registrar_saida(self, quantidade, usuario, observacao=None):
        quantidade = validar_quantidade(quantidade)
        if quantidade > self.quantidade_atual:  # RN01
            raise EstoqueInsuficienteError(self.nome, self.quantidade_atual)
        self.quantidade_atual -= quantidade
        return self._nova_movimentacao(TipoMovimentacao.SAIDA, quantidade, usuario, observacao)

    def _nova_movimentacao(self, tipo, quantidade, usuario, observacao):
        """Cria a movimentação na mesma sessão do produto: as duas são gravadas juntas no commit."""
        movimentacao = Movimentacao(
            produto=self,
            usuario=usuario,
            tipo=tipo,
            quantidade=quantidade,
            observacao=(observacao or "").strip() or None,
        )
        db.session.add(movimentacao)
        return movimentacao

    def __repr__(self):
        return f"<Produto {self.codigo} {self.nome}>"
