from .custom_payload import Payload, new_custom_payload


def new_string_payload(value: str) -> Payload:
    return new_custom_payload(value, "String")
