"""Leitura e validação dos campos de formulário, compartilhadas pelos controllers."""
import re
from decimal import ROUND_HALF_UP, Decimal, InvalidOperation

EMAIL_VALIDO = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
VALOR_MAXIMO = Decimal("99999999.99")  # limite de DECIMAL(10,2)
INTEIRO_MAXIMO = 1_000_000


def texto(dados, nome):
    """Valor de um campo de texto sem espaços nas pontas ('' se não enviado)."""
    return (dados.get(nome) or "").strip()


def somente_digitos(valor):
    """'12.345.678/0001-90' -> '12345678000190'"""
    return re.sub(r"\D", "", valor or "")


def ler_decimal(valor):
    """Lê preços em formato brasileiro ou internacional: '1.234,56', '12,5', '12.50', 'R$ 3'.

    Campo vazio vale 0,00. Lança ValueError com a mensagem para o usuário.
    """
    limpo = (valor or "").replace("R$", "").replace(" ", "")
    if not limpo:
        return Decimal("0.00")
    if "," in limpo:
        limpo = limpo.replace(".", "").replace(",", ".")
    try:
        numero = Decimal(limpo)
    except InvalidOperation:
        raise ValueError("Informe um valor válido (ex.: 12,50).") from None
    if not numero.is_finite():
        raise ValueError("Informe um valor válido (ex.: 12,50).")
    if numero < 0:
        raise ValueError("O valor não pode ser negativo.")  # M30
    if numero > VALOR_MAXIMO:
        raise ValueError("Valor muito alto.")
    return numero.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def ler_inteiro_nao_negativo(valor):
    """Lê um inteiro igual ou maior que zero. Campo vazio vale 0. Lança ValueError."""
    limpo = (valor or "").strip()
    if not limpo:
        return 0
    if not limpo.isdecimal():
        raise ValueError("Informe um número inteiro igual ou maior que zero.")
    numero = int(limpo)
    if numero > INTEIRO_MAXIMO:
        raise ValueError("Número muito alto.")
    return numero


def padrao_busca(termo):
    """Monta o padrão do LIKE tratando % e _ digitados pelo usuário como texto comum."""
    escapado = termo.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")
    return f"%{escapado}%"
