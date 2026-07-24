import json

from pydantic import ValidationError

from exceptions.ai_exception import AIResponseFormatException


def parse_ai_response(response: str, schema):
    try:
        data = json.loads(response)
        return schema(**data)

    except (json.JSONDecodeError, ValidationError):
        raise AIResponseFormatException()