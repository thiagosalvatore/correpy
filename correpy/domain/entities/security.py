import re
from dataclasses import dataclass


@dataclass
class Security:
    name: str

    def __post_init__(self) -> None:
        self.__cleanup_name()

    def __cleanup_name(self) -> None:
        self.name = re.sub(r"#[a-zA-z0-9]*", "", self.name)
        self.name = re.sub(r" D$", "", self.name)
        self.name = self.name.replace("EDJ", "").replace("EDR", "").replace(" EJ", "").replace(" ED", "")
        self.name = self.name.replace(" CI", "").replace(" ER", "")
        self.name = self.name.replace(" EB", "").replace(".", "")
        self.name = self.name.strip()
