from datetime import datetime

from pydantic import BaseModel


class UserBase(BaseModel):
    telegram_id: int


class UserCreate(UserBase):
    pass


class UserRead(UserBase):
    id: int

    updated_at: datetime
    created_at: datetime

    model_config = {
        "from_attributes": True,
    }
