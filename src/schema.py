from types import FunctionType
from typing import Type

from flask import Blueprint
from pydantic import BaseModel

from src.endpoint import EndpointMeta


class Schema:
    def __init__(self, blueprint: Blueprint, tags: list[str]):
        self.blueprint = blueprint
        self.tags = tags
        self.endpoints: list[EndpointMeta] = []

    def register_endpoint(
        self,
        name: str | None = None,
        body: Type[BaseModel] | list[Type[BaseModel]] | None = None,
    ):
        def inner(func: FunctionType):
            # Registers the endpoint metadata
            self.endpoints.append(
                EndpointMeta(name or func.__name__, func.__name__, body)
            )
            return func

        return inner
