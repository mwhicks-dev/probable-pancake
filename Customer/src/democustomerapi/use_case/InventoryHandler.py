from AbstractInventoryService import AbstractInventoryService

from entity import Inventory

class InventoryHandler:

    _inv_service: AbstractInventoryService | None = None

    def __init__(self, inv_service: AbstractInventoryService):
        self._inv_service = inv_service

    def _validate_id(self, id: int):
        if id is None:
            raise ValueError("Must supply ID")
    
    def _read_inventory(self, id: int):
        item: Inventory | None = self._inv_service.read_inventory(id)
        if item is None:
            raise ValueError(f"No item with found with id {id}")
        return item
    
    def add_new_item(self, inv: Inventory) -> None:
        if inv.id is None:
            raise ValueError("New inventory item must have ID from data warehouse")

        collision: Inventory | None = self._inv_service.read_inventory(inv.id)
        if collision is not None:
            raise ValueError("This item has already been added to inventory")
        
        self._inv_service.create_inventory(inv)
    
    def read_item_quantity(self, id: int) -> int:
        self._validate_id(id)
        item: Inventory = self._read_inventory(id)
    
        return item.quantity
    
    def add_new_stock(self, id: int, quantity: int) -> None:
        self._validate_id(id)
        item: Inventory = self._read_inventory(id)

        item.quantity += quantity

        self._inv_service.update_inventory(id, item)
    
    def remove_stock(self, id: int, quantity: int) -> None:
        self._validate_id(id)
        item: Inventory = self._read_inventory(id)

        if quantity > item.quantity:
            raise ValueError(f"Insufficient remaining quantity {item.quantity} to remove {quantity}")
        
        item.quantity -= quantity

        self._inv_service.update_inventory(id, item)