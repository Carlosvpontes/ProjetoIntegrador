"""Erros de regra de negócio. As mensagens seguem o catálogo da IHC (docs/situacao-1/03-ihc-prototipo.md)."""


class RegraDeNegocioError(Exception):
    """Base para violações das regras de negócio (RN)."""


class QuantidadeInvalidaError(RegraDeNegocioError):
    """RN02: quantidade deve ser um inteiro maior que zero."""

    def __init__(self):
        super().__init__("Informe uma quantidade inteira maior que zero.")  # M20


class EstoqueInsuficienteError(RegraDeNegocioError):
    """RN01: saída maior que o estoque disponível."""

    def __init__(self, nome_produto, disponivel):
        self.disponivel = disponivel
        super().__init__(  # M21
            f'Estoque insuficiente: há apenas {disponivel} unidade(s) de "{nome_produto}".'
        )
