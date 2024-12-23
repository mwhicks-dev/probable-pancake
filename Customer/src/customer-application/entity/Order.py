from sqlmodel import Field, SQLModel

ORDER_STATUS_V1 = ("placed", "packaged", "picked_up")

class Order(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    pickup_name: str = Field(default=None)
    pickup_dob: str = Field(default=None)
    status: str = Field(default=ORDER_STATUS_V1[0])

    __tablename__ = "order"