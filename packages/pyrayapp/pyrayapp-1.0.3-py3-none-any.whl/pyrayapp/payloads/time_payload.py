from datetime import datetime
from .payload import Payload


def new_time_payload(dt: datetime, fmt: str) -> Payload:
    return Payload(
        type="carbon",
        content={
            "formatted": dt.strftime(fmt),
            "timestamp": int(dt.timestamp()),
            "timezone": dt.astimezone().tzname()
        }
    )
