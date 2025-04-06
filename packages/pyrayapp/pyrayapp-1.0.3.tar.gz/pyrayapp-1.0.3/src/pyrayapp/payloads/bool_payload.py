from .custom_payload import Payload, new_custom_payload


def new_bool_payload(value: bool) -> Payload:
    return new_custom_payload(value, "Boolean")
