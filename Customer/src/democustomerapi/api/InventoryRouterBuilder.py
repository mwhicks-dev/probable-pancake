from fastapi import APIRouter, HTTPException

from democustomerapi.schema.NewInventoryDto import NewInventoryDto
from democustomerapi.schema.ItemIdentifier import ItemIdentifier
from democustomerapi.use_case.InventoryHandler import InventoryHandler
from democustomerapi.use_case.AbstractInventoryService import AbstractInventoryService
from democustomerapi.api.IRouterBuilder import IRouterBuilder

class InventoryRouterBuilder(IRouterBuilder):

    inventory_handler: InventoryHandler

    def __init__(self, inventory_service: AbstractInventoryService):
        self.inventory_handler = InventoryHandler(inventory_service)
    
    def _add_new_inventory(self, dto: NewInventoryDto) -> None:
        raise HTTPException(status_code=501)

    def _get_item_specifiers(self) -> list[ItemIdentifier]:
        raise HTTPException(status_code=501)

    def _get_item_quantity(self, id: int) -> int:
        raise HTTPException(status_code=501)

    def _add_stock(self, id: int, quantity: int) -> None:
        raise HTTPException(status_code=501)

    def _remove_stock(self, id: int, quantity: int) -> None:
        raise HTTPException(status_code=501)
    
    def build_router(self) -> APIRouter:
        router: APIRouter = APIRouter()
        router.add_api_route("/1/inventory", self._add_new_inventory, methods=["POST"])
        router.add_api_route("/1/inventory", self._get_item_specifiers, methods=["GET"])
        router.add_api_route("/1/inventory/{id}", self._get_item_quantity, methods=["GET"])
        router.add_api_route("/1/inventory/{id}/add/{quantity}", self._add_stock, methods=["PUT"])
        router.add_api_route("/1/inventory/{id}/remove/{quantity}", self._add_stock, methods=["PUT"])
        return router