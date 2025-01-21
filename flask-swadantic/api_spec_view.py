from flask import jsonify
from flask.views import MethodView


class APISpecsView(MethodView):
    """
    The /apispec.json and other specs
    """

    def __init__(self, *args, **kwargs):
        self.loader = kwargs.pop("loader")
        super(APISpecsView, self).__init__(*args, **kwargs)

    def get(self):
        return jsonify(self.loader())