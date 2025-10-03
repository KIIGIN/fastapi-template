from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


class UserNotFoundError(Exception):
    pass


class UserAlreadyExistsError(Exception):
    pass


def setup_exception_handlers(app: FastAPI):
    @app.exception_handler(UserNotFoundError)
    async def user_not_found_handler(request: Request, exc: UserNotFoundError):
        return JSONResponse(
            status_code=404,
            content={"error": "user_not_found", "message": str(exc)},
        )

    @app.exception_handler(UserAlreadyExistsError)
    async def user_exists_handler(request: Request, exc: UserAlreadyExistsError):
        return JSONResponse(
            status_code=400,
            content={"error": "user_exists", "message": str(exc)},
        )
