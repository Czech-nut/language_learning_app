from typing import Any

from pydantic import BaseModel as Model
from pydantic import Field

from backend.utils import snake_to_camel


class BaseModel(Model):
    class Config:
        alias_generator = snake_to_camel
        allow_population_by_field_name = True


class AuthDTO(BaseModel):
    access_token: str = Field(example="")
    refresh_token: str = Field(example="")


class SuccessResponseDTO(BaseModel):
    data: Any = None
    message: str = "Success"


class BadRequestResponse(BaseModel):
    title: str = "Bad Request"
    detail: str = "Invalid data sent to the endpoint"


class NotFoundResponse(BaseModel):
    title: str = "Not Found"
    detail: str = "Such object does not exist"


class ValidationErrorResponse(BaseModel):
    title: str = "Invalid data"
    detail: str = "Invalid data sent"


class ForbiddenResponse(BaseModel):
    title: str = "Forbidden"
    detail: str = "Not enough permissions to perform this action"


class UnauthorisedResponse(BaseModel):
    title: str = "Unauthorised"
    detail: str = "User is unauthorised"


class InternalServerErrorResponse(BaseModel):
    title: str = "Internal Server Error"
    detail: str = "Ooops! Houston we got a problem"
