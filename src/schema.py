from types import FunctionType

from flask import Blueprint


class EndpointMeta:
    def __init__(
        self,
        name: str,
        function_name: str,
    ):
        self.name = name
        self.function_name = function_name


class Schema:
    def __init__(self, blueprint: Blueprint, tags: list[str]):
        self.blueprint = blueprint
        self.tags = tags
        self.endpoints: list[EndpointMeta] = []

    def register_endpoint(
        self,
        name: str | None = None,
    ):
        def inner(func: FunctionType):
            # Registers the endpoint metadata
            self.endpoints.append(
                EndpointMeta(
                    name or func.__name__,
                    func.__name__,
                )
            )
            return func

        return inner
