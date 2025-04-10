import json
import pydantic

from loguru import logger
from pydantic.main import BaseModel

from .errors import BadRequestError, ServerError, UnsupportedMediaTypeError
from .types import Event
from .schemas import ClusterHeaders


def parse_headers(event: Event) -> ClusterHeaders:
    try:
        headers = event.get('headers', {})
        return ClusterHeaders(**headers)
    except pydantic.ValidationError as e:
        logger.error(f"Bad request: {str(e)}")
        raise UnsupportedMediaTypeError("Invalid Content-Type. Expected application/json.")
    except Exception as e:
        logger.error(f"Error parsing headers: {str(e)}")
        raise ServerError("Server error")


def parse_path(event: Event, schema: BaseModel) -> BaseModel:
    try:
        query = event.get('pathParameters', {})
        return schema(**query)
    except pydantic.ValidationError as e:
        logger.error(f"Invalid path parameters: {str(e)}")
        raise BadRequestError("Bad request", e.errors())
    except Exception as e:
        logger.error(f"Error parsing path parameters: {str(e)}")
        raise ServerError("Server error")


def parse_body(event: Event, schema: BaseModel) -> BaseModel:
    try:
        body = event.get('body', '')
        return schema(**json.loads(body))
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON: {str(e)}")
        raise BadRequestError("Invalid JSON format.", None)
    except pydantic.ValidationError as e:
        logger.error(f"Invalid body: {str(e)}")
        raise BadRequestError("Bad request", e.errors())
    except Exception as e:
        logger.error(f"Error parsing body: {str(e)}")
        raise ServerError("Server error")
