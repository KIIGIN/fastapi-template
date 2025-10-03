from sqlalchemy.exc import IntegrityError

from app.exceptions import UserAlreadyExistsError, UserNotFoundError
from app.models import User
from app.repositories.user_repo import UserRepository
from app.schemas.user import UserCreate, UserRead


class UserService:
    def __init__(self, repo: UserRepository):
        self._repo = repo

    async def add_user(self, data: UserCreate) -> UserRead:
        try:
            user = await self._repo.add(
                User(**data.model_dump(exclude_unset=True)),
            )
            await self._repo.session.commit()
        except IntegrityError:
            raise UserAlreadyExistsError(
                f"Пользователь с id={data.telegram_id} уже существует."
            )

        return UserRead.model_validate(user) if user else None

    async def get_by_telegram_id(self, telegram_id: int) -> UserRead:
        user = await self._repo.get_by_telegram_id(telegram_id)
        if not user:
            raise UserNotFoundError(f"Пользователь с id={telegram_id} не найден.")
        return UserRead.model_validate(user)
