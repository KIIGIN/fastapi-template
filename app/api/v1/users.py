from fastapi import APIRouter

from app.api.deps import UserServiceDI
from app.schemas.user import UserCreate, UserRead

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/")
async def add_user(service: UserServiceDI, data: UserCreate) -> UserRead:
    user = await service.add_user(data)
    return UserRead.model_validate(user)


@router.get("/{telegram_id}")
async def get_by_telegram_id(telegram_id: int, service: UserServiceDI) -> UserRead:
    user = await service.get_by_telegram_id(telegram_id)
    return user
