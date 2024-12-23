from abc import ABC, abstractmethod

from entity import Inventory

class AbstractInventoryService(ABC):

    @abstractmethod
    def create_inventory(inv: Inventory) -> int:
        pass

    @abstractmethod
    def read_inventory(id: int) -> Inventory:
        pass

    @abstractmethod
    def update_inventory(id: int, inv: Inventory) -> None:
        pass

    @abstractmethod
    def delete_inventory(id: int) -> None:
        pass