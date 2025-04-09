from jsonschema_rs import JSONSchema
from jsonschema_rs.error import ValidationError


def validate_json(data: dict, schema: dict) -> bool:
    try:
        schema_compiled = JSONSchema(schema)
        schema_compiled.validate(data)
        return True
    except ValidationError:
        return False
