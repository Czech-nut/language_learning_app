import asyncio
import logging

import uvicorn
from fastapi import Depends, FastAPI, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import ValidationError

from backend.database.user import create_user, retrieve_user_by_email
from backend.dtos.common import (
    AuthDTO,
    ForbiddenResponse,
    NotFoundResponse,
    SuccessResponseDTO,
    UnauthorisedResponse,
    ValidationErrorResponse,
)
from backend.dtos.user import UserIn
from backend.exceptions import Forbidden, NotFound, Unauthorised
from backend.services.auth import (
    TokenSchema,
    create_access_token,
    create_refresh_token,
    get_hashed_password,
    verify_password,
)

logger = logging.getLogger(__name__)

app = FastAPI(
    title="LLA",
    description="Language Learning App",
    version="0.1.0",
)


@app.exception_handler(NotFound)
async def not_found_error(_, e: NotFound):
    logger.warning(e)
    return JSONResponse(
        status_code=e.status,
        content=NotFoundResponse().dict(),
    )


@app.exception_handler(ValidationError)
async def validation_error(_, e: ValidationError):
    logger.warning(e)
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=ValidationErrorResponse().dict(),
    )


@app.exception_handler(Forbidden)
async def forbidden_error(_, e: Forbidden):
    logger.warning(e)
    return JSONResponse(
        status_code=e.status,
        content=ForbiddenResponse().dict(),
    )


@app.exception_handler(Unauthorised)
async def unauthorised_error(_, e: Unauthorised):
    logger.warning(e)
    return JSONResponse(
        status_code=e.status,
        content=UnauthorisedResponse().dict(),
    )


@app.get("/health", tags=["Health"])
async def check_health():
    return SuccessResponseDTO(message="I'm up!")


@app.post("/signup", tags=["Sign Up"])
async def sign_up(user_data: UserIn):
    hashed_pass = get_hashed_password(user_data.password)
    new_user = await create_user(user_data, hashed_pass)
    return SuccessResponseDTO(data=new_user)


@app.post("/login", summary="Login the user", response_model=TokenSchema)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    user_obj = await retrieve_user_by_email(form_data.username)
    if not user_obj:
        raise Forbidden()

    hashed_pass = user_obj.password
    if not verify_password(form_data.password, hashed_pass):
        raise Forbidden()

    return AuthDTO(
        access_token=create_access_token(user_obj.email),
        refresh_token=create_refresh_token(user_obj.email),
    )


async def run():
    uvicorn_config = uvicorn.Config(
        app,
        host="0.0.0.0",
        port=8000,
        lifespan="off",
        access_log=False,
        log_level="debug",
        reload=True,
    )
    server = uvicorn.Server(config=uvicorn_config)
    server.install_signal_handlers = lambda: None
    await server.serve()


if __name__ == "__main__":
    asyncio.run(run())
