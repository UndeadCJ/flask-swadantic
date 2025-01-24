from collections import defaultdict
from types import UnionType
from typing import Type, Union
from typing_extensions import get_origin, get_args

from pydantic import BaseModel

from flask_swadantic.schema import ResponseSchema
from flask_swadantic.schema import EndpointMeta
from flask_swadantic.schema import BodyType


class SchemaProcessor:
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

    def _generate_model_schema(
        self, model: Type[BaseModel] | list[Type[BaseModel]]
    ) -> dict | list[dict]:
        """
        Returns a JSON schema representation for the given model or list of models.

        Args:
            model (Union[BaseModel, List[BaseModel]]): A Pydantic model or a list of models to be processed.

        Returns:
            dict | list[dict]: Processed schema for the model(s).
        """
        if isinstance(model, list):
            return list(map(self._generate_model_schema, model))

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

        class_name = self._get_model_name(model)
        if class_name not in self._models:
            self._models.update(self._generate_model_schema(model))

        return {"$ref": f"#/components/schemas/{class_name}"}

    def _get_model_name(self, model: Type[BaseModel]):
        return model.__name__.split(".")[-1]

    def _parse_response_body(self, body: BodyType) -> dict:
        """
        Parses the `body` to produce the appropriate JSON schema representation.

        Args:
            body (BodyType): The type of the body to be parsed into a JSON schema.

        Returns:
            dict: The JSON schema representation for the provided body type.
        """
        origin = get_origin(body)

        if origin:
            if origin is list:
                parsed_items = list(map(self._parse_response_body, get_args(body)))

                if len(parsed_items) == 1:
                    items_schema = parsed_items[0]
                else:
                    items_schema = {"anyOf": parsed_items}

                return {
                    "type": "array",
                    "items": items_schema,
                }

            if origin is Union or origin is UnionType:
                union_schemas = list(map(self._parse_response_body, get_args(body)))
                return {"oneOf": union_schemas}

        if body is str:
            return {"type": "string"}
        elif isinstance(body, str):
            return {"type": "string", "const": body}
        elif body is int:
            return {"type": "integer"}
        elif isinstance(body, int):
            return {"type": "integer", "const": body}
        elif body is float:
            return {"type": "number"}
        elif isinstance(body, float):
            return {"type": "number", "const": body}
        elif body is bool:
            return {"type": "boolean"}
        elif isinstance(body, bool):
            return {"type": "boolean", "const": body}
        elif body is None:
            return {"type": "null"}
        elif body is type and issubclass(body, BaseModel):
            return self._get_model_reference(body)

        # Default empty schema if type cannot be processed
        return {}

    def _process_properties(self, properties: dict, required_fields: list[str]):
        """
        Process the properties of an object to generate query parameters.

        Args:
            properties (dict): Properties of the schema.

        Returns:
            None
        """
        query_params = []

        for field_name, field_info in properties.items():
            # Skip references for now
            if "$ref" in field_info:
                continue

            schema = {}
            if field_info.get("type") == "array":
                schema = {"type": "array", "items": field_info.get("items", {})}
            elif "anyOf" in field_info:
                schema = {"anyOf": field_info["anyOf"]}
            elif "type" in field_info:
                schema = {"type": field_info["type"], "enum": field_info.get("enum")}

            param = {
                "name": field_name,
                "in": "query",
                "schema": schema,
                "default": field_info.get("default"),
                "description": field_info.get("title", f"{field_name} query parameter"),
                "required": field_name in required_fields,
            }
            query_params.append(param)

        return query_params

    def _convert_to_openapi_query_params(self, schema: dict):
        """
        Converts a JSON schema structure into OpenAPI query parameters.

        Args:
            schema (dict): Structure with schemas in the format {"Model": {...}}.

        Returns:
            list[dict]: List of parameters in OpenAPI query parameter format.
        """
        # Process each schema in the provided JSON structure
        return self._process_properties(
            schema.get("properties", {}), schema.get("required", [])
        )

    def _map_query(self, endpoint: EndpointMeta):
        """
        Maps an endpoint's query models to OpenAPI query parameters.

        Args:
            endpoint (EndpointMeta): The endpoint for which query parameters need to be generated.

        Returns:
            list[dict]: List of OpenAPI query parameters.
        """

        # The schema is generated but not saved because it should not appear in the OpenAPI specification.
        schema = self._generate_model_schema(endpoint.query)[
            self._get_model_name(endpoint.query)
        ]
        return self._convert_to_openapi_query_params(schema)

    def _map_path(self, endpoint: EndpointMeta):
        """
        Maps an endpoint's path parameters to OpenAPI path parameters.

        Args:
            endpoint (EndpointMeta): The endpoint containing path parameters.

        Returns:
            list[dict]: List of OpenAPI path parameters.
        """
        params = []
        for param in endpoint.path:
            params.append(
                {
                    "name": param["name"],
                    "in": "path",
                    "required": True,
                    "schema": {"type": "string"},
                    "description": param["description"],
                }
            )

        return params

    def _map_body(self, endpoint: EndpointMeta):
        """
        Maps an endpoint's body schema to OpenAPI request body format.

        Args:
            endpoint (EndpointMeta): The endpoint containing the body schema.

        Returns:
            dict: OpenAPI request body content.
        """
        return {
            "content": {
                "application/json": {"schema": self._get_model_reference(endpoint.body)}
            }
        }

    def _map_response(self, response: ResponseSchema):
        return {
            response.status_code: {
                "content": {
                    "application/json": {
                        "schema": self._parse_response_body(response.body)
                    }
                }
            }
        }

    def _map_responses(self, responses: list[ResponseSchema]):
        """
        Maps a list of response schemas to OpenAPI response objects.

        Args:
            responses (list[ResponseSchema]): A list of response schemas to process.

        Returns:
            dict: OpenAPI response objects mapped by status code.
        """
        data = {}

        for response in responses:
            data.update(self._map_response(response))

        return data

    def _map_endpoint(self, endpoint: EndpointMeta):
        query_params = self._map_query(endpoint) if endpoint.query else []
        path_params = self._map_path(endpoint) if endpoint.path else []

        method = endpoint.method.lower()
        return {
            method: {
                "summary": endpoint.summary,
                "description": endpoint.description,
                "operationId": f"{endpoint.summary.lower().replace(' ', '-')}-{method}",
                "tags": endpoint.tags,
                "parameters": [*query_params, *path_params],
                "requestBody": self._map_body(endpoint) if endpoint.body else None,
                "responses": self._map_responses(endpoint.responses)
                if endpoint.responses
                else None,
            }
        }

    def _map_endpoints(self, endpoints: list[EndpointMeta]) -> dict:
        """
        Maps endpoints to the OpenAPI format.

        Args:
            endpoints (list[EndpointMeta]): List of endpoint metadata.

        Returns:
            dict: Mapped endpoints in OpenAPI format.
        """
        meta = defaultdict(dict)

        for endpoint in endpoints:
            meta[endpoint.rule].update(self._map_endpoint(endpoint))

        return meta
