import cherrypy
import os
from jsonschema import validate
from jsonschema.exceptions import ValidationError
import json
from functools import wraps


def resolve_schema(resource, verb):
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'api', 'schema', resource, verb + '.json')


def validation(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            resource, verb = f.__qualname__.lower().split('.')
            schema_path = resolve_schema(resource, verb)

            if os.path.isfile(schema_path):
                with open(schema_path, 'r') as schema:
                    schema_contents = schema.read()
                    validate(cherrypy.request.json, json.loads(schema_contents))
        except ValidationError as validation_error:
            cherrypy.response.status = 400
            return {'data': validation_error.message}

        return f(*args, **kwargs)
    return wrapper
