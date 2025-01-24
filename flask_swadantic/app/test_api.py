import enum

from flask import Blueprint
from pydantic import BaseModel

from flask_swadantic.schema.pathschema import PathSchema
from flask_swadantic.schema.response import ResponseSchema
from flask_swadantic.schema.schema import Schema

test_bp = Blueprint("test_bp", __name__)
test_schema = Schema(blueprint=test_bp, tags=["Test"])


class Test(enum.Enum):
    A = "A"
    B = "B"


class User(BaseModel):
    name: str
    email: str


class Color(BaseModel):
    user: User
    name: str = "Abacate"
    hex: str
    aba: Test = Test.A


@test_bp.get("/test/<string:name>")
@test_schema.register_endpoint(
    summary="Get Color",
    description="Test test abacate verde",
    responses=[ResponseSchema(200, Color, description="Returns a user or color")],
    tags=["Abacate"],
)
def get_test(name: str = PathSchema(description="Name of the color")):
    return f"{name}", 200


@test_bp.get("/test")
@test_schema.register_endpoint(
    summary="Get List of Color",
    description="Test test abacate verde",
    responses=[ResponseSchema(200, list[Color], description="Returns a user or color")],
    tags=["Abacate"],
)
def list_test(name: str = PathSchema(description="Name of the color")):
    return f"{name}", 200


@test_bp.post("/test")
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
    tags=["Abacate"],
)
def post_test():
    return "", 200
