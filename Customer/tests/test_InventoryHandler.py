import pytest

from democustomerapi.use_case.InventoryHandler import InventoryHandler
from democustomerapi.use_case.AbstractInventoryService import AbstractInventoryService
from democustomerapi.entity.Inventory import Inventory

from TemporaryInventoryService import TemporaryInventoryService

inventory_handler: InventoryHandler | None = None

@pytest.fixture(autouse=True)
def setup_and_breakdown():
    # global variables
    global inventory_handler

    # before
    service: AbstractInventoryService = TemporaryInventoryService()
    inventory_handler = InventoryHandler(service)

    yield

    # after
    return

def test_add_new_item():
    inv: Inventory = Inventory(id=1, name="French Press", quantity=250)
    inventory_handler.add_new_item(inv)

    assert True

@pytest.fixture
def setup_inventory():
    test_add_new_item()

def test_add_new_item_none():
    inv: Inventory = None
    with pytest.raises(ValueError):
        inventory_handler.add_new_item(inv)

def test_add_new_item_collision(setup_inventory):
    inv = Inventory(id=1, name="French Press", quantity=100)
    with pytest.raises(ValueError):
        inventory_handler.add_new_item(inv)

def test_add_new_item_no_id():
    inv: Inventory = Inventory(name="French Press", quantity=250)
    with pytest.raises(ValueError):
        inventory_handler.add_new_item(inv)

def test_read_item_quantity(setup_inventory):
    assert 250 == inventory_handler.read_item_quantity(1)

def test_read_item_quantity_notfound():
    with pytest.raises(ValueError):
        inventory_handler.read_item_quantity(1)

def test_read_item_quantity_noneid():
    with pytest.raises(ValueError):
        inventory_handler.read_item_quantity(None)

def test_add_new_stock(setup_inventory):
    inventory_handler.add_new_stock(1, 75)
    assert 325 == inventory_handler.read_item_quantity(1)

def test_add_new_stock_notfound():
    with pytest.raises(ValueError):
        inventory_handler.add_new_stock(1, 75)

def test_add_new_stock_none():
    with pytest.raises(ValueError):
        inventory_handler.add_new_stock(None, 75)

def test_add_new_stock_negative(setup_inventory):
    with pytest.raises(ValueError):
        inventory_handler.add_new_stock(1, -250)

def test_remove_stock(setup_inventory):
    inventory_handler.remove_stock(1, 35)
    assert 215 == inventory_handler.read_item_quantity(1)

def test_remove_stock_toomuch(setup_inventory):
    with pytest.raises(ValueError):
        inventory_handler.remove_stock(1, 325)

def test_remove_stock_notfound():
    with pytest.raises(ValueError):
        inventory_handler.remove_stock(1, 75)

def test_remove_stock_none():
    with pytest.raises(ValueError):
        inventory_handler.remove_stock(None, 75)

def test_remove_stock_negative(setup_inventory):
    with pytest.raises(ValueError):
        inventory_handler.remove_stock(1, -250)


