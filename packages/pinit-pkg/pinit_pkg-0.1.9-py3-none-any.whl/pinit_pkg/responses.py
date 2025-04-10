import json

from loguru import logger

def response_error(status_code: int = 500, message: str = "Server error", errors: list = None):
    logger.error(f"Error: {message}")
    body = {"message": message}

    if errors:
        body["errors"] = errors

    return {
        "statusCode": status_code,
        "body": body
    }


def handle_response(response: dict) -> dict:
    _response = {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
    }
    if isinstance(response, dict) and "statusCode" in response:
        _response["statusCode"] = response["statusCode"]
    if isinstance(response, dict) and "headers" in response:
        _response["headers"] = response["headers"]
    if isinstance(response, dict) and "body" in response:
        _response["body"] = json.dumps(response["body"])
    else:
        _response["body"] = json.dumps(response)

    return _response
