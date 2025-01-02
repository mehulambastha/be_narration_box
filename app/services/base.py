from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Type, TypeVar
from ..database import get_db

# Base service class


class BaseService:
    def __init__(self, db: AsyncSession):
        self.db = db


# Type variable for service types
ServiceType = TypeVar('ServiceType', bound=BaseService)

# Generic service factory


def get_service(service_class: Type[ServiceType]):
    def _get_service(database: AsyncSession = Depends(get_db)) -> ServiceType:
        return service_class(database)
    return _get_service
