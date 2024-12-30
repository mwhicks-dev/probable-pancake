import pytest

from fastapi import FastAPI
from fastapi.testclient import TestClient

from democustomerapi.use_case.AbstractInventoryService import AbstractInventoryService
from democustomerapi.use_case.AbstractOrderService import AbstractOrderService
from democustomerapi.use_case.AbstractOrderInventoryService import AbstractOrderInventoryService

from democustomerapi.api.IRouterBuilder import IRouterBuilder
from democustomerapi.api.InventoryRouterBuilder import InventoryRouterBuilder
from democustomerapi.api.OrderRouterBuilder import OrderRouterBuilder

from TemporaryInventoryService import TemporaryInventoryService
from TemporaryOrderInventoryService import TemporaryOrderInventoryService
from TemporaryOrderService import TemporaryOrderService

@pytest.fixture(autouse=True)
def setup_breakdown():
    # before
    inv_service: AbstractInventoryService = TemporaryInventoryService()
    order_service: AbstractOrderService = TemporaryOrderService()
    item_service: AbstractOrderInventoryService = TemporaryOrderInventoryService()
    inv_router_builder: IRouterBuilder = InventoryRouterBuilder(inv_service)
    order_router_builder: IRouterBuilder = OrderRouterBuilder(inv_service, order_service, item_service)

    app: FastAPI = FastAPI()
    app.include_router(inv_router_builder.build_router())
    app.include_router(order_router_builder.build_router())

    global client
    client = TestClient(app)

    input = {
        "id": 566,
        "name": "Mug (16oz)",
        "quantity": 505
    }
    client.post("/1/inventory", json=input)

    input = {
        "id": 723,
        "name": "French Press",
        "quantity": 250
    }
    client.post("/1/inventory", json=input)

    input = {
        "id": 50,
        "name": "Whole Medium Roast Bean",
        "quantity": 1000
    }
    client.post("/1/inventory", json=input)

    yield

    # after

def test_create_order():
    input = {
        "pickup_name": "Robert C. Martin",
        "pickup_dob": "1970/01/01",
        "items": [
            {
                "id": 723,
                "quantity": 10
            },
            {
                "id": 50,
                "quantity": 25
            }
        ]
    }

    response = client.post("/1/order", json=input)
    assert 200 == response.status_code

def test_create_order_noPickupName():
    input = {
        "pickup_dob": "1970/01/01",
        "items": [
            {
                "id": 723,
                "quantity": 10
            },
            {
                "id": 50,
                "quantity": 25
            }
        ]
    }

    response = client.post("/1/order", json=input)
    assert 422 == response.status_code

def test_create_order_noPickupDob():
    input = {
        "pickup_name": "Robert C. Martin",
        "items": [
            {
                "id": 723,
                "quantity": 10
            },
            {
                "id": 50,
                "quantity": 25
            }
        ]
    }

    response = client.post("/1/order", json=input)
    assert 422 == response.status_code

def test_create_order_noItems():
    input = {
        "pickup_name": "Robert C. Martin",
        "pickup_dob": "1970/01/01"
    }

    response = client.post("/1/order", json=input)
    assert 422 == response.status_code

def test_create_order_emptyPickupName():
    input = {
        "pickup_name": "",
        "pickup_dob": "1970/01/01",
        "items": [
            {
                "id": 723,
                "quantity": 10
            },
            {
                "id": 50,
                "quantity": 25
            }
        ]
    }

    response = client.post("/1/order", json=input)
    assert 400 == response.status_code


def test_create_order_emptyPickupDob():
    input = {
        "pickup_name": "Robert C. Martin",
        "pickup_dob": "",
        "items": [
            {
                "id": 723,
                "quantity": 10
            },
            {
                "id": 50,
                "quantity": 25
            }
        ]
    }

    response = client.post("/1/order", json=input)
    assert 400 == response.status_code

def test_create_order_emptyItems():
    input = {
        "pickup_name": "Robert C. Martin",
        "pickup_dob": "1970/01/01",
        "items": []
    }

    response = client.post("/1/order", json=input)
    assert 400 == response.status_code

def test_create_order_nullPickupName():
    input = {
        "pickup_name": None,
        "pickup_dob": "1970/01/01",
        "items": [
            {
                "id": 723,
                "quantity": 10
            },
            {
                "id": 50,
                "quantity": 25
            }
        ]
    }

    response = client.post("/1/order", json=input)
    assert 422 == response.status_code

def test_create_order_nullPickupDob():
    input = {
        "pickup_name": "Robert C. Martin",
        "pickup_dob": None,
        "items": [
            {
                "id": 723,
                "quantity": 10
            },
            {
                "id": 50,
                "quantity": 25
            }
        ]
    }

    response = client.post("/1/order", json=input)
    assert 422 == response.status_code

def test_create_order_nullItems():
    input = {
        "pickup_name": "Robert C. Martin",
        "pickup_dob": "1970/01/01",
        "items": None
    }

    response = client.post("/1/order", json=input)
    assert 422 == response.status_code

def test_create_order_wrongNameType():
    input = {
        "pickup_name": 73,
        "pickup_dob": "1970/01/01",
        "items": [
            {
                "id": 723,
                "quantity": 10
            },
            {
                "id": 50,
                "quantity": 25
            }
        ]
    }

    response = client.post("/1/order", json=input)
    assert 422 == response.status_code

def test_create_order_wrongDobType():
    input = {
        "pickup_name": "Robert C. Martin",
        "pickup_dob": 432,
        "items": [
            {
                "id": 723,
                "quantity": 10
            },
            {
                "id": 50,
                "quantity": 25
            }
        ]
    }

    response = client.post("/1/order", json=input)
    assert 422 == response.status_code

def test_create_order_wrongItemsType():
    input = {
        "pickup_name": "Robert C. Martin",
        "pickup_dob": "1970/01/01",
        "items": "test"
    }

    response = client.post("/1/order", json=input)
    assert 422 == response.status_code

def test_create_order_wrongItemIdType():
    input = {
        "pickup_name": "Robert C. Martin",
        "pickup_dob": "1970/01/01",
        "items": [
            {
                "id": "test",
                "quantity": 10
            }
        ]
    }

    response = client.post("/1/order", json=input)
    assert 422 == response.status_code

def test_create_order_wrongItemQuantityType():
    input = {
        "pickup_name": "Robert C. Martin",
        "pickup_dob": "1970/01/01",
        "items": [
            {
                "id": 723,
                "quantity": "10"
            }
        ]
    }

    response = client.post("/1/order", json=input)
    assert 422 == response.status_code

def test_create_order_noItemId():
    input = {
        "pickup_name": "Robert C. Martin",
        "pickup_dob": "1970/01/01",
        "items": [
            {
                "quantity": 10
            }
        ]
    }

    response = client.post("/1/order", json=input)
    assert 422 == response.status_code

def test_create_order_noItemQuantity():
    input = {
        "pickup_name": "Robert C. Martin",
        "pickup_dob": "1970/01/01",
        "items": [
            {
                "id": 723
            }
        ]
    }

    response = client.post("/1/order", json=input)
    assert 422 == response.status_code

def test_create_order_invalidItemId():
    input = {
        "pickup_name": "Robert C. Martin",
        "pickup_dob": "1970/01/01",
        "items": [
            {
                "id": 1,
                "quantity": 10
            }
        ]
    }

    response = client.post("/1/order", json=input)
    assert 404 == response.status_code

order_id: int = None

@pytest.fixture
def setup_order():
    input = {
        "pickup_name": "Robert C. Martin",
        "pickup_dob": "1970/01/01",
        "items": [
            {
                "id": 723,
                "quantity": 10
            },
            {
                "id": 50,
                "quantity": 25
            }
        ]
    }

    response = client.post("/1/order", json=input)
    
    global order_id
    order_id = response.json()

from democustomerapi.entity.Order import ORDER_STATUS_LATEST

def test_read_order_by_id(setup_order):
    response = client.get(f"/1/order/{order_id}")
    assert response.status_code == 200
    assert response.json() == {
        "pickup_name": "Robert C. Martin",
        "pickup_dob": "1970/01/01",
        "status": ORDER_STATUS_LATEST[0],
        "items": [
            {
                "id": 723,
                "quantity": 10
            },
            {
                "id": 50,
                "quantity": 25
            }
        ]
    }

def test_read_order_by_unknownId():
    response = client.get("/1/order/1")
    assert response.status_code == 400

def test_read_order_by_unprocessableId():
    response = client.get("/1/order/jfiosajfd")
    assert response.status_code == 422

def test_read_order_by_filters1(setup_order):
    input = {
        "last_name": "Martin",
        "dob": "1970/01/01"
    }

    response = client.get("/1/order/filter", params=input)
    assert 200 == response.status_code
    assert 1 == len(response.json())
    assert order_id in response.json()

def test_read_order_by_filters2(setup_order):
    input = {
        "last_name": "Martin",
        "dob": "1970/01/02"
    }

    response = client.get("/1/order/filter", params=input)
    assert 200 == response.status_code
    assert 0 == len(response.json())

def test_read_order_by_filters3(setup_order):
    input = {
        "last_name": "Davis",
        "dob": "1970/01/01"
    }

    response = client.get("/1/order/filter", params=input)
    assert 200 == response.status_code
    assert 0 == len(response.json())

def test_read_order_by_filters_emptyLastname(setup_order):
    input = {
        "last_name": "",
        "dob": "1970/01/01"
    }

    response = client.get("/1/order/filter", params=input)
    assert 400 == response.status_code

def test_read_order_by_filters_unprocessableName(setup_order):
    input = {
        "last_name": 182,
        "dob": "1970/01/01"
    }

    response = client.get("/1/order/filter", params=input)
    assert 422 == response.status_code

def test_read_order_by_filters_unprocessableDob(setup_order):
    input = {
        "last_name": "Martin",
        "dob": 48
    }

    response = client.get("/1/order/filter", params=input)
    assert 422 == response.status_code

def test_read_order_by_filters_noName(setup_order):
    input = {
        "dob": "1970/01/01"
    }

    response = client.get("/1/order/filter", params=input)
    assert 422 == response.status_code

def test_read_order_by_filters_noDob(setup_order):
    input = {
        "last_name": "Martin"
    }

    response = client.get("/1/order/filter", params=input)
    assert 422 == response.status_code

def test_read_order_by_filters_nullName(setup_order):
    input = {
        "last_name": None,
        "dob": "1970/01/01"
    }

    response = client.get("/1/order/filter", params=input)
    assert 422 == response.status_code

def test_read_order_by_filters_nullDob(setup_order):
    input = {
        "last_name": "Martin",
        "dob": None
    }

    response = client.get("/1/order/filter", params=input)
    assert 422 == response.status_code

def test_read_order_statuses():
    response = client.get("/1/order_statuses")
    assert 200 == response.status_code
    for i in range(0, len(response.json())):
        assert response.json()[i] == ORDER_STATUS_LATEST[i]

def test_read_order_ids_by_status(setup_order):
    response = client.get(f"/1/order/status/{ORDER_STATUS_LATEST[0]}")
    assert 200 == response.status_code
    assert 1 == len(response.json())
    assert order_id in response.json()
    for i in range(1, len(ORDER_STATUS_LATEST)):
        response = client.get(f"/1/order/status/{ORDER_STATUS_LATEST[i]}")
        assert 200 == response.status_code
        assert 0 == len(response.json())

def test_increment_order_status(setup_order):
    response = client.put(f"/1/order/{order_id}/increment")
    assert 200 == response.status_code
    response = client.get(f"/1/order/{order_id}")
    assert 200 == response.status_code
    assert ORDER_STATUS_LATEST[1] == response.json()["status"]

def test_increment_and_read_by_order_Status(setup_order):
    for i in range(1, len(ORDER_STATUS_LATEST)):
        response = client.put(f"/1/order/{order_id}/increment")
        assert 200 == response.status_code
        response = client.get(f"/1/order/status/{ORDER_STATUS_LATEST[i]}")
        assert 200 == response.status_code
        assert 1 == len(response.json())
        assert order_id in response.json()
    
    response = client.put(f"/1/order/{order_id}/increment")
    assert 400 == response.status_code
