from abc import ABC, abstractmethod

from fastapi import APIRouter

class IRouterBuilder(ABC):

    @abstractmethod
    def build_router(self) -> APIRouter:
        pass