from flask import Blueprint
from pydantic import BaseModel

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
    name="Get Color",
)
def get_test(name: str):
    return f"{name}", 200


@test_bp.post("/test/<age>")
@test_schema.register_endpoint(name="Create Color", body=[Color, User])
def post_test():
    return "", 200
