from datetime import datetime
from decimal import Decimal

from pytest import mark

from correpy.utils import extract_date_from_line, extract_value_from_line


@mark.parametrize(
    "input_string, expected_result",
    [
        ("MINERVA ON NM 2,50", Decimal("2.50")),
        ("Faria 1.200,50", Decimal("1200.50")),
        ("   1.962,90   ", Decimal("1962.90")),
        ("Idade 200  123", Decimal("200")),
        ("PETZ qtd 10", Decimal("10")),
        ("C VISTA 10,99", Decimal("10.99")),
        ("Saida 123 VISTA", Decimal("123")),
        ("Erro 13.33", Decimal("0")),
        ("Senha 1000", Decimal("0")),
        ("Zero 000###", Decimal("0")),
        ("    0.00 ", Decimal("0")),
        ("CI ER 091", Decimal("0")),
        ("Valor 0021,00", Decimal("0")),
        ("02.0", Decimal("0")),
    ],
)

def test_extract_value_from_line_when_called_then_returns_value_correctly(input_string, expected_result):
    assert extract_value_from_line(line=input_string) == expected_result


def test_extract_value_from_line_when_called_within_value_then_return_zero_value():
    assert extract_value_from_line(line="... ") == Decimal("0")


def test_extract_date_from_line_when_called_then_returns_date_correctly():
    date_string = " 03/02/2024 "
    expected_result = datetime.strptime("03/02/2024", "%d/%m/%Y").date()
    assert extract_date_from_line(line=date_string) == expected_result
