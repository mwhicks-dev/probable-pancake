import pytest
import json

from fastapi.testclient import TestClient

from democustomerapi.main import app

client: TestClient = None

@pytest.fixture(autouse=True)
def setup_breakdown():
    # before
    global client
    client = TestClient(app)

    yield

    # after

def test_create_inventory_noId():
    input = {
        "name": "French Press"
    }

    response = client.post("/1/inventory", json=input)
    assert response.status_code == 422

def test_create_inventory_noName():
    input = {
        "id": 723
    }

    response = client.post("/1/inventory", json=input)
    assert response.status_code == 422

def test_create_inventory_badNameType():
    input = {
        "id": 723,
        "name": 55
    }

    response = client.post("/1/inventory", json=input)
    assert response.status_code == 422

def test_create_inventory_badIdType():
    input = {
        "id": "723",
        "name": "French Press"
    }

    response = client.post("/1/inventory", json=input)
    assert response.status_code == 422

def test_create_inventory_negativeId():
    input = {
        "id": -723,
        "name": "French Press"
    }

    response = client.post("/1/inventory", json=input)
    assert response.status_code == 400

def test_create_inventory_emptyName():
    input = {
        "id": -723,
        "name": ""
    }

    response = client.post("/1/inventory", json=input)
    assert response.status_code == 400

def test_create_inventory_noBody():
    response = client.post("/1/inventory")
    assert response.status_code == 422

def test_create_inventory_withoutQuantity():
    input = {
        "id": 723,
        "name": "French Press"
    }

    response = client.post("/1/inventory", json=input)
    assert response.status_code == 200

def test_create_inventory_withQuantity():
    input = {
        "id": 723,
        "name": "French Press",
        "quantity": 250
    }

    response = client.post("/1/inventory", json=input)
    assert response.status_code == 200

def test_create_inventory_negativeQuantity():
    input = {
        "id": 723,
        "name": "French Press",
        "quantity": -250
    }

    response = client.post("/1/inventory", json=input)
    assert response.status_code == 400

def test_create_inventory_nullId():
    input = {
        "id": None,
        "name": "French Press",
        "quantity": 250
    }

    response = client.post("/1/inventory", json=input)
    assert response.status_code == 422

def test_create_inventory_nullName():
    input = {
        "id": 723,
        "name": None,
        "quantity": 250
    }

    response = client.post("/1/inventory", json=input)
    assert response.status_code == 422

def test_create_inventory_nullQuantity():
    input = {
        "id": None,
        "name": "French Press",
        "quantity": None
    }

    response = client.post("/1/inventory", json=input)
    assert response.status_code == 200

@pytest.fixture
def create_inventory_fixture1():
    input = {
        "id": 723,
        "name": "French Press",
        "quantity": 250
    }
    client.post("/1/inventory", json=input)

@pytest.fixture
def create_inventory_fixture2():
    input = {
        "id": 50,
        "name": "Whole Medium Roast Bean",
        "quantity": 1000
    }
    client.post("/1/inventory", json=input)

@pytest.fixture
def create_inventory_fixture3():
    input = {
        "id": 566,
        "name": "Mug (16oz)",
        "quantity": 505
    }
    client.post("/1/inventory", json=input)

def test_create_inventory_collision(create_inventory_fixture1):
    input = {
        "id": 723,
        "name": "French Press",
        "quantity": 250
    }
    response = client.post("/1/inventory", json=input)
    assert 409 == response.status_code

def test_read_all_inventory(create_inventory_fixture1, create_inventory_fixture2, create_inventory_fixture3):
    response = client.get("/1/inventory")
    assert 200 == response.status_code
    res = {}
    for entry in response.json():
        (key, value) = (entry["id"], entry["name"])
        res[key] = value
    
    assert res[723] == "French Press"
    assert res[50] == "Whole Medium Roast Bean"
    assert res[566] == "Mug (16oz)"

def test_read_quantity(create_inventory_fixture1, create_inventory_fixture2, create_inventory_fixture3):
    response = client.get("/1/inventory/723")
    assert 200 == response.status_code
    assert 250 == response.json()

    response = client.get("/1/inventory/50")
    assert 200 == response.status_code
    assert 1000 == response.json()

    response = client.get("/1/inventory/566")
    assert 200 == response.status_code
    assert 505 == response.json()

def test_read_quantity_initEmpty():
    input = {
        "id": 723,
        "name": "French Press"
    }
    client.post("/1/inventory", json=input)
    response = client.get("/1/inventory/723")
    assert 200 == response.status_code
    assert 0 == response.json()

def test_read_quantity_initNone():
    input = {
        "id": 723,
        "name": "French Press",
        "quantity": None
    }
    client.post("/1/inventory", json=input)
    response = client.get("/1/inventory/723")
    assert 200 == response.status_code
    assert 0 == response.json()

def test_read_quantity_notFound():
    response = client.get("/1/inventory/0")
    assert 404 == response.status_code

def test_read_quantity_unprocessableId():
    response = client.get("/1/inventory/fsjioifja")
    assert 422 == response.status_code

def test_add_stock(create_inventory_fixture1):
    client.put("/1/inventory/723/add/25")
    response = client.get("/1/inventory/723")
    assert 200 == response.status_code
    assert 275 == response.json()

def test_add_stock_empty(create_inventory_fixture1):
    response = client.put("/1/inventory/723/add/0")
    assert 200 == response.status_code
    response = client.get("/1/inventory/723")
    assert 200 == response.status_code
    assert 250 == response.json()

def test_add_stock_negative(create_inventory_fixture1):
    response = client.put("/1/inventory/723/add/-100")
    assert 400 == response.status_code
    response = client.get("/1/inventory/723")
    assert 200 == response.status_code
    assert 250 == response.json()

def test_add_stock_unprocessableId():
    response = client.put("/1/inventory/hfea/add/100")
    assert 422 == response.status_code

def test_add_stock_unprocessableInventory(create_inventory_fixture1):
    response = client.put("/1/inventory/723/add/fdsaf")
    assert 422 == response.status_code

def test_add_stock_idNotFound():
    response = client.put("/1/inventory/723/add/100")
    assert 404 == response.status_code

def test_remove_stock(create_inventory_fixture1):
    response = client.put("/1/inventory/723/remove/25")
    assert 200 == response.status_code
    response = client.get("/1/inventory/723")
    assert 200 == response.status_code
    assert 225 == response.json()

def test_remove_stock_empty(create_inventory_fixture1):
    response = client.put("/1/inventory/723/remove/0")
    assert 200 == response.status_code
    response = client.get("/1/inventory/723")
    assert 200 == response.status_code
    assert 250 == response.json()

def test_remove_stock_negative(create_inventory_fixture1):
    response = client.put("/1/inventory/723/remove/-100")
    assert 400 == response.status_code
    response = client.get("/1/inventory/723")
    assert 200 == response.status_code
    assert 250 == response.json()

def test_remove_stock_unprocessableId():
    response = client.put("/1/inventory/hfea/remove/100")
    assert 422 == response.status_code

def test_remove_stock_unprocessableInventory(create_inventory_fixture1):
    response = client.put("/1/inventory/723/remove/fdsaf")
    assert 422 == response.status_code

def test_remove_stock_idNotFound():
    response = client.put("/1/inventory/723/remove/100")
    assert 404 == response.status_code

def test_remove_stock_excess(create_inventory_fixture1):
    response = client.put("/1/inventory/723/remove/300")
    assert 400 == response.status_code
