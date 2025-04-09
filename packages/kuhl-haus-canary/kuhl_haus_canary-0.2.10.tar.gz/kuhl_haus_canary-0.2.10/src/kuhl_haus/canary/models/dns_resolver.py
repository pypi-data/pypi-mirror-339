import json
from dataclasses import dataclass
from typing import Any, List

from dataclasses_json import dataclass_json, LetterCase


@dataclass_json(letter_case=LetterCase.SNAKE)
@dataclass()
class DnsResolver:
    name: str
    ip_address: str


@dataclass_json(letter_case=LetterCase.SNAKE)
@dataclass()
class DnsResolverList:
    resolvers: List[DnsResolver]

    @staticmethod
    def from_file(file_path) -> List[Any]:
        try:
            with open(file_path, 'r') as file:
                file_contents = json.load(file)
                return DnsResolverList.from_dict(file_contents).resolvers
        except FileNotFoundError:
            print(f"File {file_path} not found.")
            return []
        except json.JSONDecodeError:
            print(f"Error decoding JSON from file {file_path}")
            return []
