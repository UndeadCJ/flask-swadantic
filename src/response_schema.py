from typing import Type

from pydantic import BaseModel


class ResponseSchema:
    def __init__(
        self,
        status_code: int,
        body: Type[BaseModel] | list[Type[BaseModel]] | Type[str],
        description: str | None = None,
    ):
        self.status_code = status_code
        self.body = body
        self.description = description
