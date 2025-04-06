from .custom_payload import Payload, new_custom_payload


def new_html_payload(html: str) -> Payload:
    return new_custom_payload(html, "Html")
