from fastapi import APIRouter, HTTPException

from democustomerapi.use_case.InventoryHandler import InventoryHandler
from democustomerapi.use_case.OrderHandler import OrderHandler

inventory_handler: InventoryHandler | None = None
order_handler: OrderHandler | None = None

router = APIRouter()

@router.post("/1/order")
def create_order(dto):
    raise HTTPException(status_code=501)

@router.get("/1/order/{id}")
def read_order_by_id(id: int):
    raise HTTPException(status_code=501)

@router.get("/1/order_statuses")
def read_order_statuses():
    raise HTTPException(status_code=501)

@router.get("/1/order/status/{status}")
def read_orders_by_status(status: str):
    raise HTTPException(status_code=501)

@router.get("/1/order/filter")
def read_orders_by_status(dto):
    raise HTTPException(status_code=501)

@router.put("/1/order/{id}/increment")
def increment_order_status(id: int):
    raise HTTPException(status_code=501)