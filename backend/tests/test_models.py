import pytest
from sqlalchemy.exc import IntegrityError

from app.database.models import Lesson, Progress
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

    def test_progress_cascade_deleted_for_lesson(self, db_session, user):
        """
        Progress records should be deleted if their lesson object was deleted.
        """

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

        lesson_progress = (
            db_session.query(Progress).filter(Progress.lesson_id == lesson.id).all()
        )
        assert not lesson_progress

    def test_progress_cascade_deleted_for_user(self, db_session, user):
        """
        Progress records should be deleted if their user object was deleted.
        """

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

        lesson_progress = (
            db_session.query(Progress).filter(Progress.lesson_id == lesson.id).all()
        )
        assert not lesson_progress

        db_session.delete(lesson)

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

        with pytest.raises(IntegrityError):
            lesson2 = Lesson(
                name=faker.name(),
                content=faker.text(),
                preview=faker.url(),
                order=1,
            )

            db_session.add(lesson2)
            db_session.commit()
