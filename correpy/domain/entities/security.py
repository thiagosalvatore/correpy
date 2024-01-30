import re
from dataclasses import dataclass
from typing import Optional

# 3	Ordinárias / VALE3
# 4	Preferenciais / GGBR4
# 5	Preferenciais Classe A / USIM5
# 6	Preferenciais Classe B / ELET6
# 11 BDRs, ETs e Units / BOVA11

# Format XXXXY or XXXXYF or XXXXYB where Y can be 3, 4, 11
BASIC_TICKER_PATTERN = "([A-Z-0-9]{4})(2|3|4|5|6|11|12)(F|B)?"

# Format XXXXYY where YY can be 31, 32, 33, 34, 35, 36, 39
BDR_TICKER_PATTERN = "([A-Z-0-9]{4})(31|32|33|34|35|36|39)"


@dataclass
class Security:
    name: str
    ticker: Optional[str] = None

    def __post_init__(self) -> None:
        self.__cleanup_name()
        self.ticker = self.extract_ticker_from_name()

    def __cleanup_name(self) -> None:
        self.name = re.sub(r"#[a-zA-z0-9]*", "", self.name)
        self.name = re.sub(r" D$", "", self.name)
        self.name = self.name.replace("EDJ", "").replace("EDR", "").replace(" EJ", "").replace(" ED", "")
        self.name = self.name.replace(" CI", "").replace(" ER", "")
        self.name = self.name.replace(" EB", "").replace(".", "")
        self.name = self.name.strip()

    def extract_ticker_from_name(self) -> Optional[str]:
        patterns_to_check = [BDR_TICKER_PATTERN, BASIC_TICKER_PATTERN]

        for pattern in patterns_to_check:
            if extracted_text := re.search(pattern, self.name, re.IGNORECASE):
                return extracted_text[0]
        return None
