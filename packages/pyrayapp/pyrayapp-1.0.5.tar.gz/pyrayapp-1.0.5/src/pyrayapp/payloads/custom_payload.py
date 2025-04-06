from typing import Any

from .payload import Payload

def new_custom_payload(content: Any, label: str ="") -> Payload:
    return Payload(
        type="custom",
        content={
            "content": content,
            "label": label,
        },
    )
