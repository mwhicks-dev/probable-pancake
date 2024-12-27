from abc import ABC, abstractmethod

from democustomerapi.entity.Inventory import Inventory

class AbstractInventoryService(ABC):

    @abstractmethod
    def create_inventory(self, inv: Inventory) -> int:
        pass

    @abstractmethod
    def read_inventory(self, id: int) -> Inventory:
        pass

    @abstractmethod
    def update_inventory(self, id: int, inv: Inventory) -> None:
        pass

    @abstractmethod
    def delete_inventory(self, id: int) -> None:
        pass