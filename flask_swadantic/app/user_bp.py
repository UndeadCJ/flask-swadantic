from uuid import UUID

from flask import Blueprint
from pydantic import BaseModel

from flask_swadantic.schema.path import PathSchema
from flask_swadantic.schema.response import ResponseSchema
from flask_swadantic.schema.schema import Schema

user_bp = Blueprint("user_bp", __name__, url_prefix="/users")
user_schema = Schema(blueprint=user_bp, tags=["Users"])


class User(BaseModel):
    name: str
    email: str


@user_bp.get("/<uuid:id>")
@user_schema.register_endpoint(
    summary="Get User",
    description="Returns a user by ID",
    responses=[
        ResponseSchema(200, User, description="Returns a user"),
        ResponseSchema(404, None, description="User not found"),
    ],
)
def get_user(user_id: UUID = PathSchema(description="User ID")):
    return f"{user_id}", 200


@user_bp.delete("/<uuid:id>")
@user_schema.register_endpoint(
    summary="Delete User",
    description="Deletes a user by ID",
    responses=[
        ResponseSchema(204, None),
    ],
)
def delete_user(user_id: UUID = PathSchema(description="User ID")):
    return f"{user_id}", 204


@user_bp.get("")
@user_schema.register_endpoint(
    summary="List Users",
    description="Returns a list of users",
    responses=[ResponseSchema(200, list[User])],
)
def list_users():
    return "", 200


@user_bp.post("")
@user_schema.register_endpoint(
    summary="Create User",
    description="Create a new user",
    body=User,
    responses=[
        ResponseSchema(
            200,
            User,
            description="Returns the created user",
        )
    ],
)
def create_user():
    return "", 200
