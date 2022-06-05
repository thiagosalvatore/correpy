import re
from datetime import date, datetime
from decimal import Decimal

NUMBER_STRUCTURE_REGEX = r"(?:[1-9]\d{0,2}(?:\.\d{3})*|0)(?:,\d{1,2})"
DATE_STRUCTURE_REGEX = r"[\d]{1,2}/[\d]{1,2}/[\d]{4}"


def extract_value_from_line(*, line: str) -> Decimal:
    total_value = re.findall(NUMBER_STRUCTURE_REGEX, line)
    return Decimal(total_value[0].replace(",", ".")) if total_value else Decimal(0)


def extract_date_from_line(*, line: str) -> date:
    reference_date_string = re.findall(DATE_STRUCTURE_REGEX, line)[0]
    return datetime.strptime(reference_date_string, "%d/%m/%Y").date()
