from types import FunctionType
from typing import Type

from flask import Blueprint
from pydantic import BaseModel

from src.endpoint import EndpointMeta
from src.response_schema import ResponseSchema


class Schema:
    def __init__(self, blueprint: Blueprint, tags: list[str]):
        self.blueprint = blueprint
        self.tags = tags
        self.endpoints: list[EndpointMeta] = []

    def register_endpoint(
        self,
        summary: str | None = None,
        description: str | None = None,
        body: Type[BaseModel] | list[Type[BaseModel]] | None = None,
        responses: list[ResponseSchema] | None = None,
        tags: list[str] | None = [],
    ):
        def inner(func: FunctionType):
            # Registers the endpoint metadata
            self.endpoints.append(
                EndpointMeta(
                    summary or func.__name__,
                    func.__name__,
                    description,
                    body,
                    responses,
                    tags,
                )
            )
            return func

        return inner
