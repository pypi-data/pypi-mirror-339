from .custom_payload import Payload, new_custom_payload


def new_null_payload() -> Payload:
    return new_custom_payload(None, "Null")
