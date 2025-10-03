from fastapi import FastAPI

from app.api.v1 import users
from app.exceptions import setup_exception_handlers

app = FastAPI()

setup_exception_handlers(app)

app.include_router(users.router)
