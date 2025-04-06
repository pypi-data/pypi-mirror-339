from .payload import Payload


def new_notify_payload(value: str) -> Payload:
    return Payload(
        type="notify",
        content={
            "value": value
        }
    )
