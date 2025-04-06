from .payload import Payload


def new_color_payload(color: str) -> Payload:
    return Payload(
        type="color",
        content={
            "color": color
        }
    )
