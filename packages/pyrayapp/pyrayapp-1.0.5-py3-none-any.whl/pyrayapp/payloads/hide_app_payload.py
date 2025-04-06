from .payload import Payload


def new_hide_app_payload() -> Payload:
    return Payload(
        type="hide_app"
    )
