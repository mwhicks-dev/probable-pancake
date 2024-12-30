from pydantic import BaseModel

class NewInventoryDto(BaseModel):
    id: int
    name: str
    quantity: int = 0