from flask import Blueprint

from flask_swadantic import Schema
from flask_swadantic.app.api_v1_bp import api_v1_bp, api_v1_schema

# API
api_bp = Blueprint("api", __name__, url_prefix="/api")
api_schema = Schema(api_bp)


# Registers
api_bp.register_blueprint(api_v1_bp)
api_schema.register_schema(api_v1_schema)
