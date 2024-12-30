from democustomerapi.schema.ItemQuantity import ItemQuantity

from pydantic import BaseModel

class NewOrderDto(BaseModel):
    pickup_name: str
    pickup_dob: str
    items: list[ItemQuantity]