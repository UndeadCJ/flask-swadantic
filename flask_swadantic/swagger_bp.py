from flask import Blueprint, send_file, send_from_directory

swagger_bp = Blueprint("swagger_bp", __name__)

@swagger_bp.get("")
def get_swagger():
    return send_file("templates/index.html")


@swagger_bp.get("/static")
def get_swagger_static():
    return send_from_directory("static", "/static")
