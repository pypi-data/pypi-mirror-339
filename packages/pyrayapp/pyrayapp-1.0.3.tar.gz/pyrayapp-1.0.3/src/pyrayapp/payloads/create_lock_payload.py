from .payload import Payload


def new_create_lock_payload(name: str):
    return Payload(
        type="create_lock",
        content={
            "name": name,
        }
    )
