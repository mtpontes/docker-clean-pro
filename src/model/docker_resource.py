from typing import Optional

class DockerResource:
    def __init__(self, id: str, name: str, type: str, size: Optional[str] = None, status: Optional[str] = None):
        self.id = id
        self.name = name
        self.type = type
        self.size = size
        self.status = status

    def __repr__(self):
        return f"<{self.type.capitalize()} id={self.id[:12]} name={self.name}>"
