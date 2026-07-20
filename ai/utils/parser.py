import json

from exceptions.ai_exception import AIResponseFormatException


def parse_ai_response(response: str, schema):
    try:
        data = json.loads(response)
        return schema(**data)

    except json.JSONDecodeError:
        raise AIResponseFormatException()