from functools import cached_property

from flask import Flask, Blueprint

from flask_swadantic.openapi import OpenAPIGenerator
from flask_swadantic.schema import Schema
from flask_swadantic.schema import InfoSchema
from flask_swadantic.app.api_spec_view import APISpecsView
from flask_swadantic.swagger_bp import swagger_bp


class Swadantic:
    def __init__(self, info_schema: InfoSchema, app: Flask | None = None):
        super().__init__()

        self._open_api_version = "3.1.1"
        self._info_schema = info_schema
        self._schemas: list[Schema] = []

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
        if schema not in self._schemas:
            self._schemas.append(schema)

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
            **OpenAPIGenerator().generate(self._schemas),
        }
