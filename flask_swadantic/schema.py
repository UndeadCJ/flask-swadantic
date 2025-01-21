from types import FunctionType
from typing import Type

from flask import Blueprint
from pydantic import BaseModel

from flask_swadantic.response_schema import ResponseSchema
from flask_swadantic.endpoint import EndpointMeta


class Schema:
    """Represents a schema responsible for managing API endpoints
    and their metadata in a Flask blueprint.

    This class is used to register endpoints, associate them with specific
    tags, and store their metadata for further use. Each endpoint can include
    details such as its description, query parameters, request body schema,
    response schema, and associated tags.

    Attributes:
        blueprint (Blueprint): The Flask Blueprint associated with this schema.
        tags (list[str]): A list of tags categorizing the endpoints.
        endpoints (list[EndpointMeta]): A list containing endpoint metadata.
    """

    def __init__(self, blueprint: Blueprint, tags: list[str]):
        """Initializes the Schema class.

        Args:
            blueprint (Blueprint): The Flask Blueprint associated with the schema.
            tags (list[str]): A list of tags used for categorizing the endpoints.
        """
        self.blueprint = blueprint
        self.tags = tags
        self.endpoints: list[EndpointMeta] = []

    def register_endpoint(
        self,
        summary: str | None = None,
        description: str | None = None,
        query: Type[BaseModel] | list[Type[BaseModel]] | None = None,
        body: Type[BaseModel] | list[Type[BaseModel]] | None = None,
        responses: list[ResponseSchema] | None = None,
        tags: list[str] | None = [],
    ):
        """Registers an endpoint and stores its metadata.

        This decorator is used to attach metadata to a Flask view function,
        such as its summary, description, query parameters, request body, and
        response schemas.

        Args:
            summary (str | None): A brief summary of the endpoint. Defaults to None.
            description (str | None): A detailed description of the endpoint. Defaults to None.
            query (Type[BaseModel] | list[Type[BaseModel]] | None): The query parameter models
                expected by the endpoint. Defaults to None.
            body (Type[BaseModel] | list[Type[BaseModel]] | None): The request body model(s)
                for the endpoint. Defaults to None.
            responses (list[ResponseSchema] | None): A list of expected response schemas.
                Defaults to None.
            tags (list[str] | None): A list of tags for further categorizing the endpoint.
                Defaults to an empty list.

        Returns:
            FunctionType: The original Flask view function wrapped with the metadata logic.
        """

        def inner(func: FunctionType):
            # Registers the endpoint metadata
            self.endpoints.append(
                EndpointMeta(
                    summary or func.__name__,
                    func.__name__,
                    description,
                    query,
                    [],
                    body,
                    responses,
                    tags,
                )
            )
            return func

        return inner
