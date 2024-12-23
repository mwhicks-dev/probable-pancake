from abc import ABC, abstractmethod

from entity import OrderInventory

class AbstractOrderInventoryService(ABC):

    @abstractmethod
    def set_item(item: OrderInventory) -> int:
        pass

    @abstractmethod
    def read_item_from_order(order_id: int, item_id: int) -> OrderInventory:
        pass

    @abstractmethod
    def read_items_from_order(order_id: int) -> list[OrderInventory]:
        pass

    @abstractmethod
    def delete_item_from_order(order_id: int, item_id: int) -> None:
        pass