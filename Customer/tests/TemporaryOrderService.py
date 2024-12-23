from democustomerapi.entity import Order
from democustomerapi.use_case import AbstractOrderService

class TemporaryOrderService(AbstractOrderService):

    order_map: dict[int, Order] = None

    def __init__(self):
        self.order_map = {}
    
    def create_order(self, order: Order) -> int:
        res: int = len(self.order_map)
        while res in self.order_map:
            res += 1
        order.id = res
        self.order_map[res] = order
        return res

    def read_order(self, id: int) -> Order:
        return self.order_map.get(id, None)

    def update_order(self, id: int, order: Order) -> None:
        if self.read_order(id) is None:
            return
        order.id = id
        self.order_map[id] = order

    def delete_order(self, id: int) -> None:
        if self.read_order(id) is None:
            return
        del self.order_map[id]