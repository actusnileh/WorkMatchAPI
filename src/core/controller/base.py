from typing import (
    Any,
    Generic,
    Type,
    TypeVar,
)
from uuid import UUID

from core.database import (
    Base,
    Propagation,
    Transactional,
)
from core.exceptions import NotFoundException
from core.repository import BaseRepository


ModelType = TypeVar("ModelType", bound=Base)


class BaseController(Generic[ModelType]):
    def __init__(self, model: Type[ModelType], repository: BaseRepository):
        self.model_class = model
        self.repository = repository

    async def get_by_id(self, id_: int, join_: set[str] | None = None) -> ModelType:
        db_obj = await self.repository.get_by(
            field="o_id",
            value=id_,
            join_=join_,
            unique=True,
        )
        if not db_obj:
            raise NotFoundException(
                f"{self.model_class.__tablename__.title()} with id: {id} does not exist",
            )

        return db_obj

    async def get_by_uuid(self, uuid: UUID, join_: set[str] | None = None) -> ModelType:
        db_obj = await self.repository.get_by(
            field="uuid",
            value=uuid,
            join_=join_,
            unique=True,
        )
        if not db_obj:
            raise NotFoundException(
                f"{self.model_class.__tablename__.title()} with id: {uuid} does not exist",
            )
        return db_obj

    async def get_all(
        self,
        skip: int = 0,
        limit: int = 100,
        join_: set[str] | None = None,
    ) -> list[ModelType]:
        response = await self.repository.get_all(skip, limit, join_)
        return response

    @Transactional(propagation=Propagation.REQUIRED)
    async def create(self, attributes: dict[str, Any]) -> ModelType:
        create = await self.repository.create(attributes)
        return create

    @Transactional(propagation=Propagation.REQUIRED)
    async def delete(self, model: ModelType) -> bool:
        delete = await self.repository.delete(model)
        return delete
