from pydantic import Field

from backend.dtos.common import BaseDTO

EMAIL_REGEX = r"^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,4}$"
HEX_REGEX = r"#?([\da-fA-F]{2})([\da-fA-F]{2})([\da-fA-F]{2})"


class Avatar(BaseDTO):
    background: str = Field(..., regex=HEX_REGEX, example="#ff0000")
    emoji: str = Field(..., example="bison")


class UserIn(BaseDTO):
    email: str = Field(
        ...,
        min_length=7,
        max_length=256,
        regex=EMAIL_REGEX,
        example="someuser@gmail.com",
    )
    password: str = Field(..., min_length=8, max_length=64, example="123456")


class UserOut(BaseDTO):
    email: str = Field(
        ...,
        min_length=7,
        max_length=256,
        regex=EMAIL_REGEX,
        example="someuser@gmail.com",
    )
    avatar: Avatar()
    streak: int = Field(..., ge=0, example="21")
