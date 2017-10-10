from jsonschema import validate
from jsonschema.exceptions import ValidationError
import pprint


schema = {
    "type": "object",
    "properties": {
        "price": {"type": "number"},
        "name": {"type": "string"}
    }
}

try:
    validate({"name": "Eggs", "price": 34.99}, schema)
    validate({"name": 100, "price": "Invalid"}, schema)
except ValidationError as value_error:
    print(value_error.message)

    print(value_error.absolute_path)
    print(value_error.absolute_schema_path)

    print(value_error.args)
    print(value_error.cause)
    print(value_error.context)
    print(value_error.instance)
    print(value_error.parent)
    print(value_error.path)
    print(value_error.relative_path)
    print(value_error.relative_schema_path)
    print(value_error.schema)
    print(value_error.schema_path)
    print(value_error.validator)
    print(value_error.validator_value)
