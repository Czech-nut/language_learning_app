import pytest as pytest
from fastapi.testclient import TestClient

from app.app import app
from app.database.models import Exercise, Lesson
from app.dtos.exercise import ExerciseType
from app.settings import Settings
from tests import db, faker


@pytest.fixture(scope="module")
def settings():
    return Settings()


@pytest.fixture(scope="module")
def client():
    client = TestClient(app)
    return client


@pytest.fixture(scope="module")
def db_session():
    with db.get_db_session() as session:
        yield session


@pytest.fixture(scope="session", autouse=True)
def faker_seed():
    return 123456789


@pytest.fixture(scope="function")
def lesson_with_exercise(db_session):
    lesson = Lesson(
        name=faker.name(),
        content=faker.text(),
        preview=faker.url(),
        order=0,
    )
    db_session.add(lesson)
    db_session.commit()
    db_session.refresh(lesson)

    exercise = Exercise(
        lesson_id=lesson.id,
        type=ExerciseType.FREE.value,
        definition=faker.name(),
        text=faker.text(),
        link=faker.url(),
        answers=faker.first_name(),
    )
    db_session.add(exercise)
    db_session.commit()

    yield lesson
    db_session.delete(exercise)
    db_session.delete(lesson)
    db_session.commit()
