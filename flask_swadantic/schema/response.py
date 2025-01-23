from typing import Type, Union

from pydantic import BaseModel


BodyType = (
    Type[BaseModel]
    | list[Type[BaseModel]]
    | Union[Type[BaseModel], Type[BaseModel]]
    | Union[Type[BaseModel], list[Type[BaseModel]]]
    | Union[Type[BaseModel], str]
    | Union[Type[BaseModel], list[str]]
    | Union[Type[BaseModel], int]
    | Union[Type[BaseModel], list[int]]
    | Union[str, int]
    | Union[list[str], int]
    | Union[list[str], list[int]]
    | Union[str, list[int]]
    | Type[str]
    | Type[list[str]]
)


class ResponseSchema:
    def __init__(
        self,
        status_code: int,
        body: BodyType,
        description: str | None = None,
    ):
        self.status_code = status_code
        self.body = body
        self.description = description
