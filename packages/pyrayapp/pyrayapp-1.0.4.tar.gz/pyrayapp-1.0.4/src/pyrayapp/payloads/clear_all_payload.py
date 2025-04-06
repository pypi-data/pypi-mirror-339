from .payload import Payload

def new_clear_all_payload():
    return Payload(
        type="clear_all"
    )
