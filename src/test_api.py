from flask import Blueprint

from src.schema import Schema

test_bp = Blueprint("test_bp", __name__)
test_schema = Schema(blueprint=test_bp, tags=["Test"])


class Path:
    def __init__(self, description: str):
        self.description = description


@test_bp.get("/test/<string:name>")
@test_schema.register_endpoint(
    name="Pegar abacate",
)
def get_test(name: str):
    return f"{name}", 200


@test_bp.post("/test/<age>")
@test_schema.register_endpoint(
    name="Criar abacate",
)
def post_test(age: int):
    return "", 200
