import pytest

from democustomerapi.entity.Inventory import Inventory
from democustomerapi.entity.Order import Order, ORDER_STATUS_LATEST
from democustomerapi.entity.OrderInventory import OrderInventory

from democustomerapi.use_case.OrderHandler import OrderHandler
from democustomerapi.use_case.InventoryHandler import InventoryHandler

from TemporaryInventoryService import TemporaryInventoryService
from TemporaryOrderService import TemporaryOrderService
from TemporaryOrderInventoryService import TemporaryOrderInventoryService

order_handler: OrderHandler | None = None

@pytest.fixture(autouse=True)
def setup_and_breakdown():
    global order_handler

    # before
    inventory_handler: InventoryHandler = InventoryHandler(inv_service=TemporaryInventoryService())
    order_handler = OrderHandler(inv_handler=inventory_handler, 
                                 item_service=TemporaryOrderInventoryService(), 
                                 order_service=TemporaryOrderService())
    
    inventory_handler.add_new_item(
        Inventory(id=1, name="French Press", quantity=250)
    )
    inventory_handler.add_new_item(
        Inventory(id=2, name="Chemex", quantity=775)
    )
    inventory_handler.add_new_item(
        Inventory(id=3, name="Coffee Syphon", quantity=115)
    )

    yield

    # after
    return

def test_create_new_order():
    id: int = order_handler.create_new_order(
        order=Order(pickup_name="Mason", pickup_dob="1970/01/01"),
        items={
            1: 125,
            3: 50
        }
    )

    assert id is not None
    assert type(id) == int
    assert id >= 0

order_id: int | None = None

@pytest.fixture
def setup_order():
    global order_id
    order_id = order_handler.create_new_order(
        order=Order(pickup_name="Mason", pickup_dob="1970/01/01"),
        items={
            1: 125,
            3: 50
        }
    )

def test_create_new_order_noneOrder():
    with pytest.raises(ValueError):
        order_handler.create_new_order(
            order=None,
            items={1:125}
        )

def test_create_new_order_noneitems():
    with pytest.raises(ValueError):
        order_handler.create_new_order(
            order=Order(pickup_name="Mason", pickup_dob="1970/01/01"),
            items=None
        )

def test_create_new_order_invaliditems():
    with pytest.raises(ValueError):
        order_handler.create_new_order(
            order=Order(pickup_name="Mason", pickup_dob="1970/01/01"),
            items={4:75}
        )

def test_create_new_order_emptyitems():
    with pytest.raises(ValueError):
        order_handler.create_new_order(
            order=Order(pickup_name="Mason", pickup_dob="1970/01/01"),
            items={}
        )

def test_create_new_order_negativeamt():
    with pytest.raises(ValueError):
        order_handler.create_new_order(
            order=Order(pickup_name="Mason", pickup_dob="1970/01/01"),
            items={1:-75}
        )

def test_create_new_order_0amt():
    with pytest.raises(ValueError):
        order_handler.create_new_order(
            order=Order(pickup_name="Mason", pickup_dob="1970/01/01"),
            items={1:0}
        )

def test_read_order_by_id(setup_order):
    order: Order = order_handler.read_order_by_id(order_id)

    assert "Mason" == order.pickup_name
    assert "1970/01/01" == order.pickup_dob
    assert ORDER_STATUS_LATEST[0] == order.status

def test_read_order_by_id_invalid():
    with pytest.raises(ValueError):
        order_handler.read_order_by_id(41)

def test_read_order_by_id_None():
    with pytest.raises(ValueError):
        order_handler.read_order_by_id(None)

def test_read_order_items_by_id(setup_order):
    items: list[OrderInventory] = order_handler.read_order_items_by_id(order_id)
    item_map: dict[int, OrderInventory] = {}
    for item in items:
        assert item.order_id == order_id
        item_map[item.item_id] = item
    
    assert 2 == len(items)
    assert 1 in item_map and 3 in item_map
    assert item_map[1].quantity == 125
    assert item_map[3].quantity == 50

def test_read_order_items_by_id_invalid():
    with pytest.raises(ValueError):
        order_handler.read_order_items_by_id(41)

def test_read_order_items_by_id_None():
    with pytest.raises(ValueError):
        order_handler.read_order_items_by_id(None)

def test_update_order_item1(setup_order):
    order_handler.update_order_item(
        order_id, OrderInventory(order_id=order_id, item_id=2, quantity=33)
    )

    items: list[OrderInventory] = order_handler.read_order_items_by_id(order_id)
    item_map: dict[int, OrderInventory] = {}
    for item in items:
        assert item.order_id == order_id
        item_map[item.item_id] = item
    
    assert 3 == len(items)
    assert 1 in item_map and 2 in item_map and 3 in item_map
    assert item_map[1].quantity == 125
    assert item_map[2].quantity == 33
    assert item_map[3].quantity == 50

def test_update_order_item1(setup_order):
    order_handler.update_order_item(
        order_id, OrderInventory(order_id=order_id, item_id=1, quantity=0)
    )

    items: list[OrderInventory] = order_handler.read_order_items_by_id(order_id)
    item_map: dict[int, OrderInventory] = {}
    for item in items:
        assert item.order_id == order_id
        item_map[item.item_id] = item
    
    assert 1 == len(items)
    assert 3 in item_map
    assert item_map[3].quantity == 50

def test_update_order_invalidid():
    with pytest.raises(ValueError):
        order_handler.update_order_item(
            1, OrderInventory(order_id=1, item_id=1, quantity=0)
        )

def test_update_order_Noneid():
    with pytest.raises(ValueError):
        order_handler.update_order_item(
            None, OrderInventory(order_id=None, item_id=1, quantity=0)
        )

def test_update_order_Noneitem(setup_order):
    with pytest.raises(ValueError):
        order_handler.update_order_item(
            order_id, None
        )

def test_update_order_negquantity(setup_order):
    with pytest.raises(ValueError):
        order_handler.update_order_item(
            order_id, OrderInventory(order_id=order_id, item_id=1, quantity=-25)
        )

def test_update_order_invaliditemid(setup_order):
    with pytest.raises(ValueError):
        order_handler.update_order_item(
            order_id, OrderInventory(order_id=order_id, item_id=5, quantity=0)
        )

def test_get_possible_statuses():
    assert list(ORDER_STATUS_LATEST) == order_handler.get_possible_statuses()

def test_increment_order_status(setup_order):
    for index in range(0, len(ORDER_STATUS_LATEST) - 1):
        assert ORDER_STATUS_LATEST[index] == order_handler.read_order_by_id(order_id).status
        order_handler.increment_order_status(order_id)
    assert ORDER_STATUS_LATEST[-1] == order_handler.read_order_by_id(order_id).status
    with pytest.raises(ValueError):
        order_handler.increment_order_status(order_id)