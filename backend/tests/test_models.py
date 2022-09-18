from app.database.models import Lesson


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

    def test_progress_cascade_deleted_for_lesson(self):
        """
        Progress records should be deleted if their lesson object was deleted.
        """
        pass

    def test_progress_cascade_deleted_for_user(self):
        """
        Progress records should be deleted if their user object was deleted.
        """
        pass

    def test_lesson_order_unique(self):
        """
        Lessons should have unique order number.
        """
        pass
