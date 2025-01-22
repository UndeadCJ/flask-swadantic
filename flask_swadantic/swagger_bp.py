import os

from flask import Blueprint, send_file, send_from_directory

swagger_bp = Blueprint("swagger_bp", __name__, static_folder="static")


@swagger_bp.get("")
def get_swagger():
    filepath = os.path.join(swagger_bp.root_path, "templates", "index.html")
    return send_file(filepath)


@swagger_bp.get("/static/<path:filename>")
def get_swagger_static(filename):
    static_folder = os.path.join(swagger_bp.root_path, "static")
    return send_from_directory(static_folder, filename)
