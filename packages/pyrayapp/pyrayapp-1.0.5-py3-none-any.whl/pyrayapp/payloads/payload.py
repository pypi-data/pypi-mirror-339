from typing import Dict, Any


class Payload:
    def __init__(self, type, content: Any | None = None, origin: Any = None):
        self.type = type
        self.content = content
        self.origin = origin

    def to_dict(self) -> Dict:
        return {
            "type": self.type,
            "content": self.content,
            "origin": self.origin
        }
