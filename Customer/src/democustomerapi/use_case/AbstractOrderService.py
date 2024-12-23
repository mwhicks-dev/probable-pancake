from abc import ABC, abstractmethod

from entity import Order

class AbstractOrderService(ABC):

    @abstractmethod
    def create_order(order: Order) -> int:
        pass

    @abstractmethod
    def read_order(id: int) -> Order:
        pass

    @abstractmethod
    def update_order(id: int, order: Order) -> None:
        pass

    @abstractmethod
    def delete_order(id: int) -> None:
        pass