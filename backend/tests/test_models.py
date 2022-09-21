from sqlalchemy.orm.exc import ObjectDeletedError

from app.database.models import Lesson, Progress, User
from tests import faker


class TestModels:
    def test_delete_lesson_with_exercises(self, db_session, lesson_with_exercise):
        """
        If we delete a lesson with exercises linked, we should delete the lesson,
        but not delete exercises. Just unlink them from the lesson.
        """
        lesson_id = lesson_with_exercise.id
        exercises = lesson_with_exercise.exercises
        db_session.delete(lesson_with_exercise)
        db_session.commit()

        assert not exercises[0].lesson_id
        deleted_lesson = (
            db_session.query(Lesson.id).where(Lesson.id == lesson_id).first()
        )
        assert not deleted_lesson

    def test_progress_cascade_deleted_for_lesson(self, db_session):
        """
        Progress records should be deleted if their lesson object was deleted.
        """

        user = User(
            id=1,
            email=faker.email(),
            background=faker.color(),
            emoji=faker.color(),
            password=faker.password(),
            streak=1,
        )

        db_session.add(user),
        db_session.commit(),
        db_session.refresh(user)

        lesson = Lesson(
            name=faker.name(),
            content=faker.text(),
            preview=faker.url(),
            order=0,
        )
        db_session.add(lesson)
        db_session.commit()
        db_session.refresh(lesson)

        progress = Progress(
            user_id=user.id,
            lesson_id=lesson.id,
        )

        db_session.add(progress)
        db_session.commit()

        assert progress

        db_session.delete(lesson)
        db_session.commit()

        try:
            assert not progress.lesson_id
        except ObjectDeletedError:
            db_session.delete(user)
            db_session.commit()
            return 0

    def test_progress_cascade_deleted_for_user(self, db_session):
        """
        Progress records should be deleted if their user object was deleted.
        """
        user = User(
            id=1,
            email=faker.email(),
            background=faker.color(),
            emoji=faker.color(),
            password=faker.password(),
            streak=1,
        )

        db_session.add(user),
        db_session.commit(),
        db_session.refresh(user)

        lesson = Lesson(
            name=faker.name(),
            content=faker.text(),
            preview=faker.url(),
            order=0,
        )
        db_session.add(lesson)
        db_session.commit()
        db_session.refresh(lesson)

        progress = Progress(
            user_id=user.id,
            lesson_id=lesson.id,
        )

        db_session.add(progress)
        db_session.commit()

        assert progress

        db_session.delete(user)
        db_session.commit()

        try:
            assert not progress.lesson_id
        except ObjectDeletedError:
            db_session.delete(lesson)
            db_session.commit()
            return 0

    def test_lesson_order_unique(self, db_session):
        """
        Lessons should have unique order number.
        """

        lesson1 = Lesson(
            name=faker.name(),
            content=faker.text(),
            preview=faker.url(),
            order=1,
        )
        db_session.add(lesson1)
        db_session.commit()
        db_session.refresh(lesson1)

        is_order_unique1 = lesson1.__table__.columns.get("order")

        assert is_order_unique1

        lesson2 = Lesson(
            name=faker.name(),
            content=faker.text(),
            preview=faker.url(),
            order=1,
        )
        db_session.add(lesson2)
        db_session.commit()
        db_session.refresh(lesson2)

        is_order_unique2 = lesson2.__table__.columns.get("order")

        assert not is_order_unique2

        db_session.delete(lesson1)
        db_session.delete(lesson2)
        db_session.commit()
