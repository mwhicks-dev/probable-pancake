from pydantic import BaseModel

class ItemQuantity(BaseModel):
    id: int
    quantity: int