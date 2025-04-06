from .payload import Payload


def new_new_screen_payload(name: str) -> Payload:
    return Payload(
        type="new_screen",
        content={
            "name": name,
        },
    )
