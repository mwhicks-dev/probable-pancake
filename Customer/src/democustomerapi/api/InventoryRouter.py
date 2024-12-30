from fastapi import APIRouter, HTTPException

from democustomerapi.use_case.InventoryHandler import InventoryHandler

inventory_handler: InventoryHandler | None = None

router = APIRouter()

@router.post("/1/inventory")
def add_new_inventory(dto):
    raise HTTPException(status_code=501)

@router.get("/1/inventory")
def get_item_specifiers():
    raise HTTPException(status_code=501)

@router.get("/1/inventory/{id}")
def get_item_quantity(id: int):
    raise HTTPException(status_code=501)

@router.put("/1/inventory/{id}/add/{quantity}")
def add_stock(id: int, quantity: int):
    raise HTTPException(status_code=501)

@router.put("/1/inventory/{id}/remove/{quantity}")
def remove_stock(id: int, quantity: int):
    raise HTTPException(status_code=501)