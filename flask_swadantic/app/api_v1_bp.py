# V1
from flask import Blueprint

from flask_swadantic import Schema
from flask_swadantic.app.test_api import test_bp, test_schema

api_v1_bp = Blueprint("api_v1", __name__, url_prefix="/v1")
api_v1_bp.register_blueprint(test_bp)

# V1 Schema
api_v1_schema = Schema(api_v1_bp)
api_v1_schema.register_schema(test_schema)
