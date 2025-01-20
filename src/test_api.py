from flask import Blueprint
from pydantic import BaseModel

from src.response_schema import ResponseSchema
from src.schema import Schema

test_bp = Blueprint("test_bp", __name__)
test_schema = Schema(blueprint=test_bp, tags=["Test"])


class User(BaseModel):
    name: str
    email: str


class Color(BaseModel):
    user: User
    name: str
    hex: str


@test_bp.get("/test/<string:name>")
@test_schema.register_endpoint(
    summary="Get Color",
    description="Test test abacate verde",
    responses=[
        ResponseSchema(200, [Color, User], description="Returns a user or color")
    ],
    tags=["Abacate"],
)
def get_test(name: str):
    return f"{name}", 200


@test_bp.post("/test/<age>")
@test_schema.register_endpoint(
    summary="Create Color",
    description="",
    body=[Color, User],
    responses=[ResponseSchema(200, str, description="Returns a success message")],
    tags=["Abacate"],
)
def post_test():
    return "", 200
