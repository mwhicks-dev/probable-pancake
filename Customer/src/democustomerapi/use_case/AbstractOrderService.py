from abc import ABC, abstractmethod

from democustomerapi.entity.Order import Order

class AbstractOrderService(ABC):

    @abstractmethod
    def create_order(self, order: Order) -> int:
        pass

    @abstractmethod
    def read_order(self, id: int) -> Order:
        pass

    @abstractmethod
    def update_order(self, id: int, order: Order) -> None:
        pass

    @abstractmethod
    def delete_order(self, id: int) -> None:
        pass