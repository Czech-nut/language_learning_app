from enum import Enum

from pydantic import Field

from backend.dtos.common import BaseModel


class ExerciseType(Enum):
    FREE = "free"
    MULTIPLE_CHOICE = "multiple-choice"


class ExerciseDTO(BaseModel):
    id: int = Field()
    type: ExerciseType = Field(example="multiple-choice")
    definition: str = Field(max_length=512, example="Choose correct option:")
    text: str = Field(max_length=2048, example="John _ never been to Japan.")
    link: str | None = Field(
        None, max_length=512, example="https://s3-link.com/lesson1.png"
    )
    option_a: str | None = Field(None, example="has")
    option_b: str | None = Field(None, example="have")
    option_c: str | None = Field(None, example="had")
    option_d: str | None = Field(None, example="was")
    answers: str | None = Field(max_length=2048, example="has;has yet")
