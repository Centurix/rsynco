import cherrypy
import os
from jsonschema import Draft4Validator
import json
from functools import wraps
import logging
from pathlib import Path


def resolve_schema(resource, verb):
    return Path(os.path.dirname(os.path.realpath(__file__)), '..', 'api', 'schema', resource, verb + '.json')


def validation(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        resource, verb = f.__qualname__.lower().split('.')
        schema_path = resolve_schema(resource, verb)

        logging.debug('Validating resource {} for verb {} using {} '.format(resource, verb, schema_path))

        if schema_path.is_file():
            with schema_path.open('r') as schema:
                schema_contents = schema.read()
                validator = Draft4Validator(json.loads(schema_contents))
                errors = list()
                for validation_error in sorted(validator.iter_errors(cherrypy.request.json), key=str):
                    path = list(validation_error.path)
                    logging.debug(path)
                    errors.append({
                        "status": "400",
                        "title": validation_error.message,
                        "path": '/'.join(str(x) for x in path),
                        "validator": validation_error.validator,
                        "validator_value": validation_error.validator_value
                    })
                if len(errors) > 0:
                    logging.debug('Found {} validation errors'.format(len(errors)))
                    cherrypy.response.status = 400
                    return {
                        'errors': errors
                    }
        else:
            logging.debug('No JSON SCHEMA document found, not validating')

        logging.debug('No validation errors found')
        return f(*args, **kwargs)
    return wrapper
