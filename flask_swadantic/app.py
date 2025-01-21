from flask import Flask

from flask_swadantic.info_schema import InfoSchema
from flask_swadantic.swadantic import Swadantic
from flask_swadantic.test_api import test_bp, test_schema

app = Flask(__name__)
swadantic = Swadantic(
    InfoSchema(
        title="Test API",
        version="1.0.0",
        description="Test API description",
    ),
    app,
)

app.register_blueprint(test_bp)
swadantic.register_schema(test_schema)

if __name__ == "__main__":
    app.run()
