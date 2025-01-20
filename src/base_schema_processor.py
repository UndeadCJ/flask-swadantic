from typing import Type

from pydantic import BaseModel


class BaseSchemaProcessor:
    def __init__(self):
        self._models = {}

    def _parse_defs(self, schema: dict) -> dict:
        """
        Parses and processes `$defs` from a schema for JSON Schema.

        Args:
            schema (dict): Schema containing `$defs`.

        Returns:
            dict: Parsed schema components.
        """
        # JSON Schema 2020-12 specs
        # https://tour.json-schema.org/content/06-Combining-Subschemas/01-Reusing-and-Referencing-with-defs-and-ref

        parsed_schema = {}
        defs = schema.pop("$defs", {})
        for key in defs:
            parsed_schema[defs[key]["title"]] = defs[key]
        return parsed_schema

    def _get_model_schema(self, model) -> dict | list[dict]:
        """
        Returns a JSON schema representation for the given model or list of models.

        Args:
            model (Union[BaseModel, List[BaseModel]]): A Pydantic model or a list of models to be processed.

        Returns:
            dict | list[dict]: Processed schema for the model(s).
        """
        if isinstance(model, list):
            return list(map(self._get_model_schema, model))

        schema = model.model_json_schema(ref_template="#/components/schemas/{model}")
        parsed_schema = self._parse_defs(schema)
        parsed_schema[schema["title"]] = schema
        return parsed_schema

    def _get_model_reference(
        self, model: Type[BaseModel] | list[Type[BaseModel]]
    ) -> dict:
        """
        Creates a JSON Schema reference for the response model.

        Args:
            model (Union[Type[BaseModel], List[Type[BaseModel]]]):
                A single response model type or a list of response model types.

        Returns:
            dict: JSON Schema `$ref` or `oneOf` for the specified response model(s).
        """
        if isinstance(model, list):
            return {"oneOf": list(map(self._get_model_reference, model))}

        class_name = model.__name__.split(".")[-1]
        return {"$ref": f"#/components/schemas/{class_name}"}

    def update_model_schemas(self, schemas: dict):
        """
        Updates the internal models dictionary with new schemas.

        Args:
            schemas (dict): Dictionary of schemas to add.
        """
        self._models.update(schemas)
