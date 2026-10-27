from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app.extensions import db
from app.models.base import agora


class Usuario(UserMixin, db.Model):
    """Pessoa que acessa o sistema."""

    __tablename__ = "usuario"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)  # RN08
    senha_hash = db.Column(db.String(255), nullable=False)
    criado_em = db.Column(db.DateTime, nullable=False, default=agora)

    movimentacoes = db.relationship("Movimentacao", back_populates="usuario", passive_deletes="all")

    def definir_senha(self, senha):
        """Guarda apenas o hash da senha, nunca a senha em texto puro (RNF04)."""
        self.senha_hash = generate_password_hash(senha)

    def verificar_senha(self, senha):
        return check_password_hash(self.senha_hash, senha)

    def __repr__(self):
        return f"<Usuario {self.email}>"
