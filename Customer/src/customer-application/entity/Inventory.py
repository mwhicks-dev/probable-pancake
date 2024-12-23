from sqlmodel import Field, SQLModel

class Inventory(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str = Field(default=None, index=True)
    quantity: int = Field(default=0)

    __tablename__ = "inventory"