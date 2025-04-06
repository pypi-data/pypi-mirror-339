from .payload import Payload


def new_size_payload(color: str):
    return Payload(
        type="size",
        content={
            "color": color
        }
    )
