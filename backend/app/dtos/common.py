from typing import Any

from pydantic import BaseModel, Field

from backend.utils import snake_to_camel


class AuthDTO(BaseModel):
    access_token: str = Field(example="")
    refresh_token: str = Field(example="")


class BaseDTO(BaseModel):
    class Config:
        alias_generator = snake_to_camel
        allow_population_by_field_name = True


class SuccessResponseDTO(BaseModel):
    data: Any = None
    message: str = "Success"


class BadRequestResponse(BaseDTO):
    title: str = "Bad Request"
    detail: str = "Invalid data sent to the endpoint"


class NotFoundResponse(BaseDTO):
    title: str = "Not Found"
    detail: str = "Such object does not exist"


class ValidationErrorResponse(BaseDTO):
    title: str = "Invalid data"
    detail: str = "Invalid data sent"


class ForbiddenResponse(BaseDTO):
    title: str = "Forbidden"
    detail: str = "Not enough permissions to perform this action"


class UnauthorisedResponse(BaseDTO):
    title: str = "Unauthorised"
    detail: str = "User is unauthorised"


class InternalServerErrorResponse(BaseDTO):
    title: str = "Internal Server Error"
    detail: str = "Ooops! Houston we got a problem"
