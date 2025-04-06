from .payload import Payload


def new_show_app_payload() -> Payload:
    return Payload(
        type="show_app"
    )
