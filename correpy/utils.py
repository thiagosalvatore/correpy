import re
from datetime import date, datetime
from decimal import Decimal

NUMBER_STRUCTURE_REGEX = r"(?<![\d(\.|,)])(?:0,\d{2}|[1-9]\d{0,2}(?:\.\d{3})*,\d{2}|[1-9]\d{0,2})(?![\d(\.|,)])"
AMOUNT_STRUCTURE_REGEX = r"(?<![\d.,])(?:0|[1-9]\d{0,2}(?:\.\d{3})*|\d+)(?![\d.,])"
DATE_STRUCTURE_REGEX = r"[\d]{1,2}/[\d]{1,2}/[\d]{4}"
ID_STRUCTURE_REGEX = r"^\D*(\d+)"


def extract_value_from_line(*, line: str) -> Decimal:
    if total_value := re.findall(NUMBER_STRUCTURE_REGEX, line):
        return Decimal(total_value[-1].replace(".", "").replace(",", "."))

    return Decimal(0)


def extract_amount_from_line(*, line: str) -> Decimal:
    if total_value := re.findall(AMOUNT_STRUCTURE_REGEX, line):
        return Decimal(total_value[-1].replace(".", ""))

    return Decimal(0)


def extract_date_from_line(*, line: str) -> date:
    if date_matches := re.findall(DATE_STRUCTURE_REGEX, line):
        return datetime.strptime(date_matches[0], "%d/%m/%Y").date()
    return date.today()  # Return today's date as a fallback


def extract_id_from_line(*, line: str) -> int:
    """Extraction of the note id (number)"""
    return int(re.search(ID_STRUCTURE_REGEX, line).group(1))
