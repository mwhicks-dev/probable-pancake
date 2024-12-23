from democustomerapi.entity import OrderInventory
from democustomerapi.use_case import AbstractOrderInventoryService

class TemporaryOrderInventoryService(AbstractOrderInventoryService):

    item_map: dict[tuple[int, int], OrderInventory] = None

    def set_item(self, item: OrderInventory) -> int:
        key: tuple[int, int] = (item.order_id, item.item_id)
        self.item_map[key] = item

    def read_item_from_order(self, order_id: int, item_id: int) -> OrderInventory:
        key: tuple[int, int] = (order_id, item_id)
        return self.item_map.get(key, None)

    def read_items_from_order(self, order_id: int) -> list[OrderInventory]:
        res: list[OrderInventory] = []
        for (key, value) in self.item_map.items():
            if key[0] != order_id:
                continue
            res.append(value)
        return res

    def delete_item_from_order(self, order_id: int, item_id: int) -> None:
        key: tuple[int, int] = (order_id, item_id)
        if key not in self.item_map:
            return
        del self.item_map[key]
