from app.extensions import db


class Fornecedor(db.Model):
    """Empresa que fornece produtos."""

    __tablename__ = "fornecedor"
    __table_args__ = (
        db.CheckConstraint("cnpj IS NULL OR length(cnpj) = 14", name="ck_fornecedor_cnpj"),
    )

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    cnpj = db.Column(db.String(14), unique=True)  # somente os 14 dígitos
    telefone = db.Column(db.String(20))
    email = db.Column(db.String(120))

    produtos = db.relationship("Produto", back_populates="fornecedor", passive_deletes="all")

    def pode_excluir(self):
        """RN06: fornecedor com produtos vinculados não pode ser excluído."""
        return len(self.produtos) == 0

    def __repr__(self):
        return f"<Fornecedor {self.nome}>"
