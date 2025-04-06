from typing import Any

from .payload import Payload

def new_json_string_payload(value: Any) -> Payload:
    from json import dumps, JSONDecodeError
    try:
        if isinstance(value, (list, dict)):
            value = dumps(value)
    except JSONDecodeError:
        value = str(value)
    
    return Payload(
        type="json_string",
        content={
            "value": value
        }
    )
