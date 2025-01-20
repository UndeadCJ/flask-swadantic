from typing import Type

from pydantic import BaseModel


class EndpointMeta:
    def __init__(
        self,
        name: str,
        function_name: str,
        body: Type[BaseModel] | list[Type[BaseModel]] | None = None,
        rule: str | None = None,
        method: str | None = None,
    ):
        self.name = name
        self.function_name = function_name
        self.body = body
        self.rule = rule
        self.method = method


class Endpoint:
    def __init__(self):
        self.rule = None
        self.endpoint = None
        self.method = None
        self.function_name = None

    def add_url_rule(
        self, rule, endpoint, view_func, provide_automatic_options=True, **options
    ):
        self.rule = rule
        self.endpoint = endpoint
        self.method = options.get("methods")[0]
        self.function_name = view_func.__name__
