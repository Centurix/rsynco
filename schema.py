from jsonschema import Draft4Validator
from jsonschema import validate
from jsonschema.exceptions import ValidationError
import pprint


schema = {
  "$schema": "http://json-schema.org/draft-04/schema#",
  "definitions": {},
  "properties": {
    "data": {
      "properties": {
        "attributes": {
          "properties": {
            "host": {"type": "string", "minLength": 1},
            "hostname": {"type": "string", "minLength": 1},
            "password": {"type": "string", "minLength": 1},
            "port": {"type": "integer", "minLength": 1},
            "username": {"type": "string", "minLength": 1}
          },
          "type": "object",
          "required": ["host", "hostname", "password", "port", "username"]
        },
        "type": {"type": "string"}
      },
      "type": "object",
      "required": ["attributes"]
    }
  },
  "type": "object",
  "required": ["data"],
  "additionalProperties": False
}


# validate({"name": "Eggs", "price": 34.99}, schema)
validator = Draft4Validator(schema)
for err in sorted(validator.iter_errors({
    "data": {
        "type": "hosts",
        "attributes": {
            "host": '',
            "hostname": '',
            "port": 0,
            "username": '',
            "password": ''
        }
    }
}), key=str):
    print(err.path)
    print(err.validator)
    print(err.validator_value)
    print(err.message)
    print('=====================')
