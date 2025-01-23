class QuerySchema:
    def __init__(
        self, name: str, description: str | None = None, required: bool = False
    ):
        self.name = name
        self.description = description
        self.required = required
