from flask import Flask

from flask_swadantic.app.api_bp import api_bp, api_schema
from flask_swadantic.schema.info import InfoSchema
from flask_swadantic.swadantic import Swadantic
from flask_swadantic.app.test_bp import test_bp

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
app.register_blueprint(api_bp)
swadantic.register_schema(api_schema)


if __name__ == "__main__":
    app.run()
