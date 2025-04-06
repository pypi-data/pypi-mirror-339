from .payload import Payload


def new_remove_payload() -> Payload:
    return Payload(
        type="remove"
    )
