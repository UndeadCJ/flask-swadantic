from functools import cached_property

from flask import Flask, Blueprint

from src.api_spec_view import APISpecsView
from src.info_schema import InfoSchema
from src.schema import Schema
from src.swagger_bp import swagger_bp


class Swadantic:
    def __init__(self, info_schema: InfoSchema, app: Flask | None = None):
        self._open_api_version = "3.1.1"
        self._info_schema = info_schema
        self._schemas: list[Schema] = []

        if app is not None:
            self.init_app(app)

    def init_app(self, app: Flask):
        if not app or not isinstance(app, Flask):
            raise TypeError("Invalid Flask app instance.")

        # Swagger Blueprint
        app.register_blueprint(swagger_bp, url_prefix="/swagger")

        # OpenAPI JSON Spec Blueprint
        spec_bp = Blueprint("spec_bp", __name__)
        spec_bp.add_url_rule(
            "",
            "apispec",
            view_func=APISpecsView.as_view("apispec", loader=lambda: self._get_spec),
        )
        app.register_blueprint(spec_bp, url_prefix="/apispec")

    @cached_property
    def _get_spec(self):
        return {
            "openapi": self._open_api_version,
            "info": self._info_schema,
        }

    def register_schema(self, schema: Schema):
        self._schemas.append(schema)
