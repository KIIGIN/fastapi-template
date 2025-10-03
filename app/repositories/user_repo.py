from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User
from app.repositories.base_repo import BaseRepository


class UserRepository(BaseRepository[User]):
    def __init__(self, session: AsyncSession):
        super().__init__(User, session)

    async def get_by_telegram_id(self, telegram_id: int) -> User | None:
        result = await self.get_by_filters(
            User.telegram_id == telegram_id,
        )
        return result or None
