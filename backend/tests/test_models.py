import pytest
from sqlalchemy.exc import IntegrityError

from app.database.models import Exercise, Lesson, Progress
from app.dtos.exercise import ExerciseType
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
        lesson_1 = Lesson(
            name=faker.name(),
            content=faker.text(),
            preview=faker.url(),
            order=0,
        )
        db_session.add(lesson_1)
        db_session.commit()

        lesson_2 = Lesson(
            name=faker.name(),
            content=faker.text(),
            preview=faker.url(),
            order=lesson_1.order,
        )
        db_session.add(lesson_2)
        with pytest.raises(IntegrityError):
            db_session.commit()

        db_session.rollback()
        db_session.delete(lesson_1)
        db_session.commit()

    def test_answer_field_constreint(self, lesson, db_session):
        """
        For field answers field type have to by FREE
        """

        exercise = Exercise(
            lesson_id=lesson.id,
            type=ExerciseType.MULTIPLE_CHOICE.value,
            definition=faker.name(),
            text=faker.text(),
            link=faker.url(),
            answers=faker.first_name(),
        )
        db_session.add(exercise)

        with pytest.raises(IntegrityError):
            db_session.commit()

        db_session.rollback()
        db_session.delete(lesson)
        db_session.commit()

    def test_option_fields_constreint(self, lesson, db_session):
        """
        Field type have to by MULTIPLE_CHOICE for fields option_a and option_b
        """

        exercise = Exercise(
            lesson_id=lesson.id,
            type=ExerciseType.FREE.value,
            definition=faker.name(),
            text=faker.text(),
            link=faker.url(),
            option_a=faker.first_name(),
            option_b=faker.first_name(),
            option_c=faker.first_name(),
            option_d=faker.first_name(),
        )
        db_session.add(exercise)

        with pytest.raises(IntegrityError):
            db_session.commit()

        db_session.rollback()
        db_session.delete(lesson)
        db_session.commit()
