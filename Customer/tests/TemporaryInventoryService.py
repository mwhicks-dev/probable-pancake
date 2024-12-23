from democustomerapi.entity import Inventory
from democustomerapi.use_case import AbstractInventoryService

class TemporaryInventoryService(AbstractInventoryService):

    inventory_map: dict[int, Inventory] = None

    def __init__(self):
        self.inventory_map = {}

    def create_inventory(self, inv: Inventory) -> int:
        res: int = len(self.inventory_map)
        while res in self.inventory_map:
            res += 1
        self.inventory_map[res] = inv
        inv.id = res
        return res

    def read_inventory(self, id: int) -> Inventory:
        return self.inventory_map.get(id, None)

    def update_inventory(self, id: int, inv: Inventory) -> None:
        old: Inventory = self.read_inventory(id)
        if old is None:
            return
        inv.id = id
        self.inventory_map[id] = inv

    def delete_inventory(self, id: int) -> None:
        old: Inventory = self.read_inventory(id)
        if old is not None:
            del self.inventory_map[id]
