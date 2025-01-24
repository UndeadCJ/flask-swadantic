import enum

from flask import Blueprint
from pydantic import BaseModel

from flask_swadantic.schema.path import PathSchema
from flask_swadantic.schema.response import ResponseSchema
from flask_swadantic.schema.schema import Schema

test_bp = Blueprint("test_bp", __name__, url_prefix="/test")
test_schema = Schema(blueprint=test_bp, tags=["Test"])


class Test(enum.Enum):
    A = "A"
    B = "B"


class Color(BaseModel):
    name: str = "Abacate"
    hex: str
    aba: Test = Test.A


@test_bp.get("/<string:name>")
@test_schema.register_endpoint(
    summary="Get Color",
    description="Test test abacate verde",
    responses=[ResponseSchema(200, Color, description="Returns a user or color")],
)
def get_test(name: str = PathSchema(description="Name of the color")):
    return f"{name}", 200


@test_bp.get("")
@test_schema.register_endpoint(
    summary="Get List of Color",
    description="Test test abacate verde",
    responses=[ResponseSchema(200, list[Color], description="Returns a user or color")],
)
def list_test(name: str = PathSchema(description="Name of the color")):
    return f"{name}", 200


@test_bp.post("")
@test_schema.register_endpoint(
    summary="Create Color",
    description="",
    body=Color,
    responses=[
        ResponseSchema(
            200,
            list[str, float, bool] | Color,
            description="Returns a success message",
        )
    ],
)
def post_test():
    return "", 200


@test_bp.get("health")
@test_schema.register_endpoint(
    summary="Health Check",
    description="Test test abacate verde",
    responses=[ResponseSchema(200, "OK", description="Returns a success message")],
)
def health_check():
    return "OK", 200
