from sqlmodel import Field, SQLModel

ORDER_STATUS_V1 = ("placed", "packaged", "picked_up")
ORDER_STATUS_LATEST = ORDER_STATUS_V1

class Order(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    pickup_name: str = Field()
    pickup_dob: str = Field()
    status: str = Field(default=ORDER_STATUS_LATEST[0])

    __tablename__ = "order"