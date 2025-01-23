from flask_swadantic.schema import EndpointMeta
from flask_swadantic.schema import SchemaProcessor
from flask_swadantic.schema import Schema


class OpenAPIGenerator(SchemaProcessor):
    """
    OpenAPIGenerator processes and generates OpenAPI specifications for a set of schemas.

    This class extends the functionality of SchemaProcessor to map endpoints and their
    prefixes, ensuring a structured and consistent OpenAPI specification is created.
    """

    def _add_prefix_to_endpoint(self, prefixes: list[str], endpoint: EndpointMeta):
        """
        Adds prefixes to the endpoint's rule.

        Args:
            prefixes (list[str]): A list of URL prefixes to prepend to the endpoint.
            endpoint (EndpointMeta): The endpoint metadata containing the rule to update.

        Returns:
            None
        """
        rule = endpoint.rule

        for prefix in prefixes:
            if prefix:
                rule = f"{prefix.rstrip('/')}/{rule.lstrip('/')}"

        endpoint.rule = rule

    def _process_schema(self, schemas: list[Schema]) -> dict[str, list]:
        """
        Processes the provided schemas and extracts prefixes and endpoints.

        Args:
            schemas (list[Schema]): A list of Schema objects to process.

        Returns:
            dict[str, list]: A dictionary containing the extracted prefixes and endpoints.
        """
        result = {"prefix": [], "endpoints": []}
        stack = list(schemas)

        while stack:
            schema = stack.pop()
            result["prefix"].append(schema.url_prefix)
            result["endpoints"].extend(schema.endpoints)
            stack.extend(schema.schemas)

        return result

    def _map_prefixes_to_endpoints(self, schema_result: dict):
        """
        Maps all collected prefixes to their respective endpoints.

        Args:
            schema_result (dict): A dictionary containing prefixes and a list of endpoints.

        Returns:
            None
        """
        for endpoint in schema_result["endpoints"]:
            self._add_prefix_to_endpoint(schema_result["prefix"], endpoint)

    def generate(self, schemas: list[Schema]) -> dict[str, dict]:
        """
        Generates an OpenAPI specification for the given schemas.

        Args:
            schemas (list[Schema]): A list of Schema objects representing the API schemas.

        Returns:
            dict[str, dict]: A dictionary containing the OpenAPI paths and components.

        Raises:
            ValueError: If any item in 'schemas' is not an instance of the Schema class.
        """
        if not all(isinstance(schema, Schema) for schema in schemas):
            raise ValueError("All items in 'schemas' must be instances of 'Schema'")

        schema_result = self._process_schema(schemas)
        self._map_prefixes_to_endpoints(schema_result)

        return {
            "paths": self._map_endpoints(schema_result["endpoints"]),
            "components": {"schemas": self._models},
        }
