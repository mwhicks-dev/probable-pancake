from democustomerapi.use_case.InventoryHandler import InventoryHandler
from democustomerapi.use_case.AbstractOrderInventoryService import AbstractOrderInventoryService
from democustomerapi.use_case.AbstractOrderService import AbstractOrderService

from democustomerapi.entity.Order import Order
from democustomerapi.entity.OrderInventory import OrderInventory
from democustomerapi.entity.Order import ORDER_STATUS_LATEST

class OrderHandler:

    _inv_handler: InventoryHandler | None = None
    _item_service: AbstractOrderInventoryService | None = None
    _order_service: AbstractOrderService | None = None

    def __init__(self,
                 inv_handler: InventoryHandler,
                 item_service: AbstractOrderInventoryService,
                 order_service: AbstractOrderService):
        self._inv_handler = inv_handler
        self._item_service = item_service
        self._order_service = order_service

    def create_new_order(self, order: Order, items: dict[int, int]) -> int:
        id: int = self._order_service.create_order(order)

        for item in items:
            # ensure item exists
            self._inv_handler.read_item_quantity(item)

        for (item, quantity) in items.items():
            # add to order once we know all exist
            local = OrderInventory(order_id=id, item_id=item, quantity=quantity)
            self._item_service.set_item(local)

        return id
    
    def _validate_order_id(self, id: int) -> Order:
        res: Order | None = self._order_service.read_order(id)
        if res is None:
            raise ValueError("No such order")
        return res

    def read_order_by_id(self, id: int) -> Order:
        return self._validate_order_id(id)
    
    def read_order_items_by_id(self, id: int) -> list[OrderInventory]:
        self._validate_order_id(id)
        return self._item_service.read_items_from_order(id)
    
    def update_order_item(self, id: int, item: OrderInventory) -> None:
        self._validate_order_id(id)
        self._item_service.set_item(item)

    def get_possible_statuses(self) -> list[str]:
        return list(ORDER_STATUS_LATEST)
    
    def increment_order_status(self, id: int) -> None:
        order: Order = self._validate_order_id(id)
        current_status: str = order.status
        index: int = ORDER_STATUS_LATEST.index(current_status)
        
        if index + 1 == len(ORDER_STATUS_LATEST):
            raise ValueError("Cannot move order beyond final status")
        order.status = ORDER_STATUS_LATEST[index + 1]
        self._order_service.update_order(id, order)