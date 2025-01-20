from flask import Flask

from src.info_schema import InfoSchema
from src.swadantic import Swadantic

app = Flask(__name__)
swadantic = Swadantic(
    InfoSchema(
        title="Test API",
        version="1.0.0",
        description="Test API description",
    ),
    app,
)

if __name__ == '__main__':
    app.run()
