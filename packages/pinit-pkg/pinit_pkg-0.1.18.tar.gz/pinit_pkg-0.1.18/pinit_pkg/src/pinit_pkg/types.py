from typing import TypedDict


class Headers(TypedDict):
    content_type: str


class Event(TypedDict):
    headers: Headers
    body: str


class Context:
    aws_request_id: str

    def __init__(self, aws_request_id: str):
        self.aws_request_id = aws_request_id
