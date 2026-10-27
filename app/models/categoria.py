from app.extensions import db


class Categoria(db.Model):
    """Agrupamento de produtos (ex.: Bebidas, Limpeza)."""

    __tablename__ = "categoria"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(60), nullable=False, unique=True)
    descricao = db.Column(db.String(255))

    produtos = db.relationship("Produto", back_populates="categoria", passive_deletes="all")

    def pode_excluir(self):
        """RN06: categoria com produtos vinculados não pode ser excluída."""
        return len(self.produtos) == 0

    def __repr__(self):
        return f"<Categoria {self.nome}>"
