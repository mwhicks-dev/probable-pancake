from .Inventory import Inventory
from .Order import Order

from sqlmodel import Field, SQLModel, PrimaryKeyConstraint

class OrderInventory(SQLModel, table=True):
    order_id: int = Field(default=None, foreign_key=f"{Order.__tablename__}.id", index=True)
    item_id: int = Field(default=None, foreign_key=f"{Inventory.__tablename__}.id", index=True)
    quantity: int = Field(default=None)

    __tablename__ = "order_inventory"
    __table_args__ = (
        PrimaryKeyConstraint("order_id", "item_id"),
    )