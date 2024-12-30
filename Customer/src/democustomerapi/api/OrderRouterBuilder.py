from fastapi import APIRouter, HTTPException

from democustomerapi.schema.NewOrderDto import NewOrderDto
from democustomerapi.schema.OrderDto import OrderDto
from democustomerapi.use_case.InventoryHandler import InventoryHandler
from democustomerapi.use_case.OrderHandler import OrderHandler
from democustomerapi.use_case.AbstractInventoryService import AbstractInventoryService
from democustomerapi.use_case.AbstractOrderInventoryService import AbstractOrderInventoryService
from democustomerapi.use_case.AbstractOrderService import AbstractOrderService
from democustomerapi.api.IRouterBuilder import IRouterBuilder

class OrderRouterBuilder(IRouterBuilder):

    inventory_handler: InventoryHandler
    order_handler: OrderHandler

    def __init__(self, inventory_service: AbstractInventoryService, 
                 order_service: AbstractOrderService, 
                 item_service: AbstractOrderInventoryService):
        self.inventory_handler = InventoryHandler(inventory_service)
        self.order_handler = OrderHandler(self.inventory_handler, 
                                          item_service, order_service)
    
    def _create_order(self, dto: NewOrderDto) -> int:
        raise HTTPException(status_code=501)

    def _read_order_by_id(self, id: int) -> OrderDto:
        raise HTTPException(status_code=501)

    def _read_order_statuses(self) -> list[str]:
        raise HTTPException(status_code=501)

    def _read_orders_by_status(self, status: str) -> list[int]:
        raise HTTPException(status_code=501)

    def _read_orders_by_filter(self, last_name: str, dob: str) -> list[int]:
        raise HTTPException(status_code=501)

    def _increment_order_status(self, id: int) -> None:
        raise HTTPException(status_code=501)
    
    def build_router(self) -> APIRouter:
        router: APIRouter = APIRouter()
        router.add_api_route("/1/order", self._create_order, methods=["POST"])
        router.add_api_route("/1/order/{id}", self._read_order_by_id, methods=["GET"])
        router.add_api_route("/1/order_statuses", self._read_order_statuses, methods=["GET"])
        router.add_api_route("/1/order/status/{status}", self._read_orders_by_status, methods=["GET"])
        router.add_api_route("/1/order/filter", self._read_orders_by_filter, methods=["GET"])
        router.add_api_route("/1/order/{id}/increment", self._increment_order_status, methods=["PUT"])
        return router
