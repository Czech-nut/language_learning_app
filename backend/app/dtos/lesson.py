from typing import List

from pydantic import Field

from app.dtos.common import BaseModel


class LessonMinimal(BaseModel):
    id: int = Field()
    name: str = Field(min_length=3, max_length=1024, example="Past Simple")
    content: str = Field(example="Past Simple is used for past!")


class LessonDTO(BaseModel):
    id: int = Field()
    completed: bool = Field(False)
    preview: str = Field(example="https://s3-link.com/my-preview.png")
    name: str = Field(example="Past Simple")


class LessonsList(BaseModel):
    streak: int = Field()
    lessons: List[LessonDTO] = Field([])
