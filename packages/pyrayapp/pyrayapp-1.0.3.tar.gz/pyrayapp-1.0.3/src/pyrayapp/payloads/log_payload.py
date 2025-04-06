from typing import Any

from .payload import Payload


def new_log_payload(value: Any) -> Payload:
    return Payload(
        type="log",
        content={
            "value": value,
        }
    )