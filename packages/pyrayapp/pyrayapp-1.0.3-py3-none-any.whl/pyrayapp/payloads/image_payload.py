from .custom_payload import Payload, new_custom_payload


def new_image_payload(location: str) -> Payload:
    sanitized = location.replace('"', '')
    html = f'<img src="{sanitized}" alt="" />'
    return new_custom_payload(html, "Image")
