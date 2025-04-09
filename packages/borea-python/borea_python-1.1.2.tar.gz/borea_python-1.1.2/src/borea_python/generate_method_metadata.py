from typing import Any, Callable, Dict, List, Tuple, Union

from .helpers import Helpers
from .models.handler_class_models import MethodParameter
from .models.openapi_models import HttpParameter, SchemaMetadata


class GenerateMethodMetadata:
    @classmethod
    def _get_single_nested_schema(
        cls, schema: Union[SchemaMetadata, None]
    ) -> Union[Dict[str, Any], None]:
        if schema is None:
            return None
        if schema.length_nested_json_schemas != 1:
            return schema.model_dump()
        schema = schema.model_dump()
        nested_schema = schema.get("nested_json_schemas", [None])[0]
        if nested_schema:
            return nested_schema
        return schema

    @classmethod
    def _method_params_from_http_params(
        cls, http_params: List[HttpParameter], cond: Callable[[HttpParameter], bool]
    ) -> List[MethodParameter]:
        """
        Returns a list of MethodParameter objects based on the given condition.
        """
        method_params = []
        for http_param in http_params:
            if cond(http_param):
                formatted_type, schema_type, type_is_schema = Helpers.format_type(
                    http_param.type
                )
                method_params.append(
                    MethodParameter(
                        required=http_param.required,
                        name=http_param.name,
                        original_name=http_param.original_name,
                        type=formatted_type,
                        schema_type=schema_type,
                        type_is_schema=type_is_schema or http_param.type_is_schema,
                        description=http_param.description,
                    )
                )
        return method_params

    @classmethod
    def _method_params_from_schema_props(
        cls,
        schema: Dict[str, Any],
        props: List[Dict[str, Any]],
        cond: Callable[[str, bool], bool],
    ) -> List[MethodParameter]:
        default_description = "No description provided"
        schema_required = schema.get("required", [])

        def is_required(prop_name, prop):
            return prop_name in schema_required or prop.get("required", False)

        method_params = []
        for prop_name, prop in props.items():
            if cond(prop_name, is_required(prop_name, prop)):
                formatted_type, schema_type, type_is_schema = Helpers.format_type(prop)

                # Get description with proper fallback handling
                nested_schemas = prop.get("nested_json_schemas", [schema])
                first_schema_desc = (
                    nested_schemas[0].get("description") if nested_schemas else None
                )
                description = (
                    prop.get("description") or first_schema_desc or default_description
                )

                method_params.append(
                    MethodParameter(
                        required=is_required(prop_name, prop),
                        name=prop_name,
                        type=formatted_type,
                        schema_type=schema_type,
                        type_is_schema=type_is_schema
                        or prop.get("type_is_schema", False),
                        description=description,
                    )
                )
        return method_params

    @classmethod
    def _method_param_from_request_body(
        cls, request_body: Dict[str, Any]
    ) -> List[MethodParameter]:
        formatted_type, schema_type, type_is_schema = Helpers.format_type(request_body)
        return [
            MethodParameter(
                required=request_body.get("required", False),
                name="request_body",
                type=formatted_type,
                schema_type=schema_type,
                type_is_schema=type_is_schema
                or request_body.get("type_is_schema", False),
                description=request_body.get("description", "Request body"),
            )
        ]

    @classmethod
    def resolve_method_params(
        cls, parameters: List[HttpParameter], request_body: Union[Dict[str, Any], None]
    ) -> Tuple[
        Union[Dict[str, Any], None], List[MethodParameter], List[MethodParameter]
    ]:
        required_http_params: List[
            MethodParameter
        ] = cls._method_params_from_http_params(
            parameters, lambda http_param: http_param.required
        )
        optional_http_params: List[
            MethodParameter
        ] = cls._method_params_from_http_params(
            parameters, lambda http_param: not http_param.required
        )
        http_param_names = [param.name for param in parameters]

        schema: Union[Dict[str, Any], None] = cls._get_single_nested_schema(
            request_body
        )
        required_schema_props: List[MethodParameter] = []
        optional_schema_props: List[MethodParameter] = []
        if schema is not None:
            schema_props = schema.get("properties", None)
            if schema_props:
                required_schema_props += cls._method_params_from_schema_props(
                    schema,
                    schema_props,
                    lambda prop_name, is_required: is_required
                    and prop_name not in http_param_names,
                )
                optional_schema_props += cls._method_params_from_schema_props(
                    schema,
                    schema_props,
                    lambda prop_name, is_required: not is_required
                    and prop_name not in http_param_names,
                )
            elif schema.get("required", False):
                required_schema_props += cls._method_param_from_request_body(schema)
            else:
                optional_schema_props += cls._method_param_from_request_body(schema)

        required_method_params = required_http_params + required_schema_props
        optional_method_params = optional_http_params + optional_schema_props

        return [schema, required_method_params, optional_method_params]
