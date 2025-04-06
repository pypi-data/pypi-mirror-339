from .payload import Payload


def new_clear_screen_payload() -> Payload:
    return Payload(
        type="new_screen",
        content=""
    )
