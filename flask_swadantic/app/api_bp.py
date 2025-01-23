from flask import Blueprint, jsonify

from flask_swadantic import Schema
from .test_api import test_bp, test_schema

# API
api_bp = Blueprint("api", __name__, url_prefix="/api")
api_schema = Schema(api_bp)

# V1
api_v1_bp = Blueprint("api_v1", __name__, url_prefix="/v1")
api_v1_bp.register_blueprint(test_bp)

# V1 Schema
api_v1_schema = Schema(api_v1_bp)
api_v1_schema.register_schema(test_schema)


@api_v1_bp.get("/god-of-war")
@api_v1_schema.register_endpoint(
    summary="Endpoint do God of War",
    description="Test test abacate verde",
    tags=["Abacate"],
)
def god_of_war():
    return jsonify({}), 200


# Registers
api_bp.register_blueprint(api_v1_bp)
api_schema.register_schema(api_v1_schema)
