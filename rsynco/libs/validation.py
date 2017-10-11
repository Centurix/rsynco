import cherrypy
import os
from jsonschema import Draft4Validator
import json
from functools import wraps


def resolve_schema(resource, verb):
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'api', 'schema', resource, verb + '.json')


def validation(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        resource, verb = f.__qualname__.lower().split('.')
        schema_path = resolve_schema(resource, verb)

        if os.path.isfile(schema_path):
            with open(schema_path, 'r') as schema:
                schema_contents = schema.read()
                validator = Draft4Validator(json.loads(schema_contents))
                errors = list()
                for validation_error in sorted(validator.iter_errors(cherrypy.request.json), key=str):
                    path = list(validation_error.path)
                    errors.append({
                        "status": "400",
                        "title": validation_error.message,
                        "path": '/'.join(path),
                        "validator": validation_error.validator,
                        "validator_value": validation_error.validator_value
                    })
                if len(errors) > 0:
                    cherrypy.response.status = 400
                    return {
                        'errors': errors
                    }

        return f(*args, **kwargs)
    return wrapper
