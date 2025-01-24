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

    def _process_schema(self, schema: Schema) -> list[EndpointMeta]:
        """
        Processes a schema, applying its URL prefix to its endpoints
        and recursively processing child schemas.

        Args:
            schema (Schema): The schema to process.

        Returns:
            list[EndpointMeta]: A list of processed EndpointMeta objects.
        """
        endpoints = schema.endpoints

        # Recursively process child schemas
        for sub_schema in schema.schemas:
            child_endpoints = self._process_schema(sub_schema)
            endpoints.extend(child_endpoints)

        # Process endpoints of the current schema
        for endpoint in endpoints:
            self._add_prefix_to_endpoint([schema.url_prefix], endpoint)

        return endpoints

    def _process_schemas(self, schemas: list[Schema]) -> list[EndpointMeta]:
        """
        Processes a list of schemas to generate a combined list of endpoints.

        Args:
            schemas (list[Schema]): A list of Schema objects to process.

        Returns:
            list[EndpointMeta]: A list of processed EndpointMeta objects derived from all schemas.
        """
        endpoints = []

        for schema in schemas:
            endpoints.extend(self._process_schema(schema))

        return endpoints

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

        endpoints = self._process_schemas(schemas)
        models = self._models

        return {
            "paths": self._map_endpoints(endpoints),
            "components": {"schemas": models},
        }
