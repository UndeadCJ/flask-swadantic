from collections import defaultdict
from functools import cached_property

from flask import Flask, Blueprint

from src.api_spec_view import APISpecsView
from src.base_schema_processor import BaseSchemaProcessor
from src.endpoint import Endpoint, EndpointMeta
from src.info_schema import InfoSchema
from src.schema import Schema
from src.swagger_bp import swagger_bp


class Swadantic(BaseSchemaProcessor):
    def __init__(self, info_schema: InfoSchema, app: Flask | None = None):
        super().__init__()

        self._open_api_version = "3.1.1"
        self._info_schema = info_schema
        self._view_functions = {}
        self._schemas: list[Schema] = []
        self._paths = {}

        if app is not None:
            self.init_app(app)

    def init_app(self, app: Flask):
        """
        Initializes the Flask app with required configurations.

        Args:
            app (Flask): The Flask application instance.

        Raises:
            TypeError: If the provided app is not a valid Flask instance.
        """
        if not app or not isinstance(app, Flask):
            raise TypeError(
                f"Invalid Flask app instance. Expected Flask, but received {type(app).__name__}."
            )

        # Register Swagger Blueprint
        app.register_blueprint(swagger_bp, url_prefix="/swagger")

        # Register OpenAPI JSON Specification Blueprint
        spec_bp = Blueprint("spec_bp", __name__)
        spec_bp.add_url_rule(
            "",
            "apispec",
            view_func=APISpecsView.as_view("apispec", loader=lambda: self.get_spec),
        )
        app.register_blueprint(spec_bp, url_prefix="/apispec")

    def register_schema(self, schema: Schema):
        """
        Registers a new schema and processes its endpoints.

        Args:
            schema (Schema): Schema object containing blueprint and endpoint definitions.

        Raises:
            ValueError: If the schema's blueprint does not define valid deferred functions
            ValueError: If an endpoint is not found in the schema's list of endpoints
        """
        if not hasattr(schema.blueprint, "deferred_functions") or not isinstance(
            schema.blueprint.deferred_functions, list
        ):
            raise ValueError(
                "The 'blueprint' provided in the schema does not have a valid 'deferred_functions' attribute."
            )

        for func in schema.blueprint.deferred_functions:
            # Captures Flask endpoint information
            endpoint = Endpoint()
            func(endpoint)

            # Matches function names between endpoint and schema
            endpoint_meta = next(
                (
                    meta
                    for meta in schema.endpoints
                    if meta.function_name == endpoint.function_name
                ),
                None,
            )

            if endpoint_meta is None:
                raise ValueError(
                    f"Endpoint '{endpoint.function_name}' was not found in the schema's list of endpoints."
                )

            # Update the endpoint metadata
            endpoint_meta.rule = endpoint.rule
            endpoint_meta.method = endpoint.method

        self._schemas.append(schema)

    def _map_body(self, endpoint: EndpointMeta):
        schemas = self._get_model_schema(endpoint.body)
        if isinstance(schemas, list):
            for schema in schemas:
                self.update_model_schemas(schema)
        else:
            self.update_model_schemas(schemas)

        return {
            "content": {
                "application/json": {"schema": self._get_model_reference(endpoint.body)}
            }
        }

    def _map_endpoints(self, endpoints: list[EndpointMeta]) -> dict:
        """
        Maps endpoints to the OpenAPI format.

        Args:
            endpoints (list[EndpointMeta]): List of endpoint metadata.

        Returns:
            dict: Mapped endpoints in OpenAPI format.
        """
        meta = defaultdict(dict)

        for endpoint in endpoints:
            method = endpoint.method.lower()
            meta[endpoint.rule][method] = {
                "summary": endpoint.name,
                "operationId": f"{endpoint.name.lower().replace(' ', '-')}-{method}",
                "requestBody": self._map_body(endpoint) if endpoint.body else None,
            }

        return meta

    def _map_schemas(self):
        for schema in self._schemas:
            self._paths.update(self._map_endpoints(schema.endpoints))

        return {"paths": self._paths, "components": {"schemas": self._models}}

    @cached_property
    def get_spec(self) -> dict:
        """
        Generates and returns the OpenAPI Specification for the application.

        Returns:
            dict: OpenAPI Specification in JSON format.
        """
        return {
            "openapi": self._open_api_version,
            "info": self._info_schema,
            **self._map_schemas(),
        }
