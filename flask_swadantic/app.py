from flask import Flask

from info_schema import InfoSchema
from swadantic import Swadantic
from test_api import test_bp, test_schema

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
