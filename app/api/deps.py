from typing import Annotated, Type, TypeVar

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_session
from app.repositories.user_repo import UserRepository
from app.services.user_service import UserService

T = TypeVar("T")


SessionDI = Annotated[AsyncSession, Depends(get_session)]


def build_repository(repo_class: Type[T]):
    def _get_repo(session: SessionDI) -> T:
        return repo_class(session)

    return _get_repo


def build_service(service_class: Type[T], repo_class: Type):
    def _get_service(repo: repo_class = Depends(build_repository(repo_class))):
        return service_class(repo)

    return _get_service


UserRepositoryDI = Annotated[
    UserRepository, Depends(build_repository(UserRepository))
]
UserServiceDI = Annotated[
    UserService, Depends(build_service(UserService, UserRepository))
]
