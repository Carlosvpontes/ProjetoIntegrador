"""Testes da leitura de campos de formulário e da formatação de valores."""
from decimal import Decimal

import pytest

from app.controllers.formularios import ler_decimal, ler_inteiro_nao_negativo, padrao_busca, somente_digitos
from app.formatacao import formatar_cnpj, formatar_decimal


@pytest.mark.parametrize(
    "digitado, esperado",
    [
        ("12,50", "12.50"),
        ("12.50", "12.50"),
        ("1.234,56", "1234.56"),
        ("R$ 3", "3.00"),
        ("7", "7.00"),
        ("0,005", "0.01"),
        ("", "0.00"),
        (None, "0.00"),
    ],
)
def test_ler_decimal_aceita_formatos_brasileiro_e_internacional(digitado, esperado):
    assert ler_decimal(digitado) == Decimal(esperado)


@pytest.mark.parametrize("digitado", ["abc", "12,,5", "NaN", "Infinity"])
def test_ler_decimal_rejeita_texto_invalido(digitado):
    with pytest.raises(ValueError, match="Informe um valor válido"):
        ler_decimal(digitado)


def test_ler_decimal_rejeita_negativo():
    with pytest.raises(ValueError, match="O valor não pode ser negativo."):  # M30
        ler_decimal("-5")


def test_ler_decimal_rejeita_valor_acima_do_limite_do_banco():
    with pytest.raises(ValueError):
        ler_decimal("100000000")


@pytest.mark.parametrize("digitado, esperado", [("0", 0), ("15", 15), ("", 0), (None, 0)])
def test_ler_inteiro_nao_negativo(digitado, esperado):
    assert ler_inteiro_nao_negativo(digitado) == esperado


@pytest.mark.parametrize("digitado", ["-1", "2,5", "dez", "99999999"])
def test_ler_inteiro_nao_negativo_rejeita_invalidos(digitado):
    with pytest.raises(ValueError):
        ler_inteiro_nao_negativo(digitado)


def test_somente_digitos():
    assert somente_digitos("12.345.678/0001-90") == "12345678000190"


def test_padrao_busca_trata_caracteres_especiais_como_texto():
    assert padrao_busca("50%") == "%50\\%%"
    assert padrao_busca("a_b") == "%a\\_b%"


def test_formatar_cnpj():
    assert formatar_cnpj("12345678000190") == "12.345.678/0001-90"
    assert formatar_cnpj(None) == ""


def test_formatar_decimal():
    assert formatar_decimal(Decimal("1234.5")) == "1.234,50"
