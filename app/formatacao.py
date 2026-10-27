"""Formatação de valores para exibição nas telas (registradas como filtros do Jinja)."""


def formatar_decimal(valor):
    """1234.5 -> '1.234,50'"""
    return f"{valor or 0:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def formatar_moeda(valor):
    """1234.5 -> 'R$ 1.234,50'"""
    return f"R$ {formatar_decimal(valor)}"


def formatar_data_hora(valor, formato="%d/%m/%Y %H:%M"):
    return valor.strftime(formato) if valor else ""


def formatar_cnpj(cnpj):
    """'12345678000190' -> '12.345.678/0001-90'"""
    if not cnpj or len(cnpj) != 14:
        return cnpj or ""
    return f"{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:]}"
