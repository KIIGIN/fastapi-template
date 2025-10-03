from typing import (
    Any,
    Callable,
    Generic,
    Optional,
    Sequence,
    Type,
    TypeVar,
)

from sqlalchemy import delete, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    def __init__(self, model: Type[ModelType], session: AsyncSession):
        self.model = model
        self.session = session

    # ------------------ CREATE ------------------
    async def add(self, obj_in: ModelType) -> ModelType:
        self.session.add(obj_in)
        try:
            await self.session.flush()
            await self.session.refresh(obj_in)
        except IntegrityError as e:
            await self.session.rollback()
            raise e
        return obj_in

    # ------------------ READ ------------------
    async def get_by_id(self, obj_id: Any) -> Optional[ModelType]:
        stmt = select(self.model).where(self.model.id == obj_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_filters(self, *conditions) -> Optional[ModelType]:
        """conditions: список выражений, например User.email == 'test'"""
        stmt = select(self.model).where(*conditions)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all(
        self, *conditions, offset: int = 0, limit: int = 100
    ) -> Sequence[ModelType]:
        stmt = select(self.model).where(*conditions).offset(offset).limit(limit)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    # ------------------ UPDATE ------------------
    async def _update_obj(
        self, obj: Optional[ModelType], **kwargs
    ) -> Optional[ModelType]:
        if not obj:
            return None

        for key, value in kwargs.items():
            if hasattr(obj, key):
                setattr(obj, key, value)

        try:
            await self.session.flush()
            await self.session.refresh(obj)
        except IntegrityError:
            await self.session.rollback()
            raise

        return obj

    async def update_by_id(self, obj_id: Any, **kwargs) -> Optional[ModelType]:
        obj = await self.get_by_id(obj_id)
        return await self._update_obj(obj, **kwargs)

    async def update_by_filters(self, *conditions, **kwargs) -> Optional[ModelType]:
        obj = await self.get_by_filters(*conditions)
        return await self._update_obj(obj, **kwargs)

    # ------------------ DELETE ------------------
    async def delete_by_id(self, obj_id: Any) -> bool:
        obj = await self.get_by_id(obj_id)
        if not obj:
            return False
        await self.session.delete(obj)
        await self.session.flush()
        return True

    async def delete_by_filters(self, *conditions) -> Callable[[], int]:
        stmt = delete(self.model).where(*conditions)
        result = await self.session.execute(stmt)
        await self.session.flush()
        return result.rowcount

    # ------------------ EXTRA ------------------
    async def exists(self, *conditions) -> bool:
        stmt = select(self.model).where(*conditions)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none() is not None

    async def count(self, *conditions) -> int:
        stmt = select(self.model).where(*conditions)
        result = await self.session.execute(stmt)
        return len(result.scalars().all())
