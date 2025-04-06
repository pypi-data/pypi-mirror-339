from typing import Any

from .payload import Payload

def new_json_string_payload(value: Any) -> Payload:
    from json import dumps, JSONDecodeError
    try:
        content = dumps(value, ensure_ascii=False, indent=2)
    except JSONDecodeError:
        content = str(value)
    
    return Payload(
        type="json_string",
        content={
            "value": content
        }
    )
