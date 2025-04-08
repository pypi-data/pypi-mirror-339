import json
from dataclasses import dataclass, field
from functools import lru_cache
from typing import Any, List, Optional, Sequence
from urllib import parse


@dataclass()
class EndpointModel:
    mnemonic: str
    hostname: str
    scheme: Optional[str] = "https"
    port: Optional[int] = 443
    path: Optional[str] = field(default="/")
    query: Optional[Sequence[tuple[Any, Any]]] = None
    fragment: Optional[str] = None
    healthy_status_code: Optional[int] = 200
    json_response: Optional[bool] = True
    status_key: Optional[str] = "status"
    healthy_status: Optional[str] = "OK"
    version_key: Optional[str] = "version"
    connect_timeout: Optional[float] = 7
    read_timeout: Optional[float] = 7
    ignore: Optional[bool] = False

    @staticmethod
    def from_file(file_path) -> List[Any]:
        try:
            with open(file_path, 'r') as file:
                file_contents = json.load(file)
            return [EndpointModel(**x) for x in file_contents]
        except FileNotFoundError:
            print(f"File {file_path} not found.")
            return []
        except json.JSONDecodeError:
            print(f"Error decoding JSON from file {file_path}")
            return []

    @staticmethod
    @lru_cache
    def __normalize_path(path: str) -> str:
        if not path:
            path = "/"
        elif not path.startswith("/"):
            path = f"/{path}"
        # Replace multiple slashes with a single slash
        while '//' in path:
            path = path.replace('//', '/')
        return path

    @property
    def url(self) -> str:
        path = self.__normalize_path(self.path)
        if self.query:
            query_string = parse.urlencode(self.query)
            path = parse.urljoin(path, f"?{query_string}")
        if self.fragment:
            path = parse.urljoin(path, f"#{self.fragment}")
        return f"{self.scheme}://{self.hostname}:{self.port}{path}"
