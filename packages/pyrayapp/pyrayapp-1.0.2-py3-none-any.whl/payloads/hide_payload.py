from .payload import Payload


def new_hide_payload() -> Payload:
    return Payload(
        type="hide"
    )
