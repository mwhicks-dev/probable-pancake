from pydantic import BaseModel

class ItemIdentifier(BaseModel):
    id: int
    name: str