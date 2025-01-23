from types import FunctionType
from typing import Type, Self

from flask import Blueprint
from pydantic import BaseModel

from flask_swadantic.schema import ResponseSchema
from flask_swadantic.schema import EndpointMeta, Endpoint


class Schema:
    """
    Represents a schema for organizing endpoints, tags, and associated metadata
    within a Flask blueprint. This class helps define and manage API endpoints
    and their corresponding metadata, including query parameters, request bodies,
    and response schemas.
    """

    def __init__(
        self,
        blueprint: Blueprint,
        tags: list[str] | None = [],
    ):
        """
        Initializes a Schema instance.

        Args:
            blueprint (Blueprint): The Flask blueprint associated with this schema.
            tags (list[str] | None): Optional list of tags for classifying endpoints.
        """
        self._blueprint = blueprint
        self._endpoints: list[EndpointMeta] = []
        self._title = blueprint.name
        self._tags = tags
        self._schemas: list[Self] = []

    def register_schema(self, schema: Self):
        """
        Registers a schema instance to the list of schemas.

        Args:
            schema (Self): The schema instance to register.
        """
        if schema not in self._schemas:
            self._schemas.append(schema)

    def register_endpoint(
        self,
        summary: str | None = None,
        description: str | None = None,
        query: Type[BaseModel] | list[Type[BaseModel]] | None = None,
        body: Type[BaseModel] | list[Type[BaseModel]] | None = None,
        responses: list[ResponseSchema] | None = None,
        tags: list[str] | None = [],
    ):
        """
        Registers an endpoint with metadata and extra information.

        Args:
            summary (str | None): Short summary of the endpoint.
            description (str | None): Detailed description of the endpoint.
            query (Type[BaseModel] | list[Type[BaseModel]] | None): Query parameter models.
            body (Type[BaseModel] | list[Type[BaseModel]] | None): Request body model(s).
            responses (list[ResponseSchema] | None): List of possible response schemas.
            tags (list[str] | None): Additional tags for the endpoint.

        Returns:
            FunctionType: A decorator that wraps the endpoint function.
        """

        def inner(func: FunctionType):
            self._endpoints.append(
                EndpointMeta(
                    summary=summary or func.__name__,
                    function_name=func.__name__,
                    description=description,
                    query=query,
                    path=[],
                    body=body,
                    responses=responses,
                    tags=[*self._tags, *tags],
                )
            )

            return func

        return inner

    def _find_meta(self, function_name: str):
        """
        Finds metadata for a given function by its name.

        Args:
            function_name (str): The name of the function to search metadata for.

        Returns:
            EndpointMeta | None: The metadata instance if found, otherwise None.
        """
        return next(
            (meta for meta in self._endpoints if meta.function_name == function_name),
            None,
        )

    def _prepare_endpoints(self):
        """
        Prepares and updates endpoint metadata by matching blueprint functions.

        This method iterates through deferred functions associated with the
        Flask blueprint, capturing endpoint information, and synchronizing
        them with the registered endpoint metadata.

        Returns:
            list[EndpointMeta]: Updated list of endpoint metadata.
        """
        for func in self._blueprint.deferred_functions:
            # Captures Flask endpoint information
            endpoint = Endpoint()
            func(endpoint)

            # Matches function names between endpoint and schema
            endpoint_meta = self._find_meta(endpoint.function_name)

            if endpoint_meta:
                # Update the endpoint metadata
                endpoint_meta.rule = endpoint.rule
                endpoint_meta.method = endpoint.method
                endpoint_meta.path = endpoint.path

        return self._endpoints

    @property
    def url_prefix(self):
        """
        Returns the URL prefix of the associated Flask blueprint.

        Returns:
            str: The URL prefix as a string.
        """
        return self._blueprint.url_prefix

    @property
    def endpoints(self):
        """
        Returns all prepared endpoints with their metadata.

        Returns:
            list[EndpointMeta]: List of all endpoint metadata objects.
        """
        return self._prepare_endpoints()

    @property
    def tags(self):
        """
        Returns the tags associated with the schema.

        Returns:
            list[str]: List of tags.
        """
        return self._tags

    @property
    def schemas(self):
        """
        Returns the registered schemas.

        Returns:
            list[Self]: List of registered schema instances.
        """
        return self._schemas
