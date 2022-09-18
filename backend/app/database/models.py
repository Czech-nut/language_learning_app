from sqlalchemy import CheckConstraint, Column, ForeignKey, Integer, MetaData, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from app.dtos.exercise import ExerciseType

meta = MetaData(
    naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }
)
Base = declarative_base(metadata=meta)


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(256), nullable=False)
    background = Column(String(7), nullable=False)
    emoji = Column(String(24), nullable=False)
    password = Column(String(256), nullable=False)
    streak = Column(Integer, nullable=False)


class Lesson(Base):
    __tablename__ = "lesson"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(1024), nullable=False)
    content = Column(String, nullable=False)
    order = Column(Integer, unique=True, nullable=False, autoincrement=True)
    preview = Column(String, nullable=False)
    exercises = relationship("Exercise", back_populates="lesson")


class Progress(Base):
    __tablename__ = "progress"

    user_id = Column(
        Integer,
        ForeignKey(User.id, ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    )
    lesson_id = Column(
        Integer, ForeignKey(Lesson.id, ondelete="CASCADE"), nullable=False
    )


class Exercise(Base):
    __tablename__ = "exercise"

    id = Column(Integer, primary_key=True, autoincrement=True)
    lesson_id = Column(Integer, ForeignKey(Lesson.id))
    lesson = relationship(Lesson, back_populates="exercises")
    type = Column(
        String(128),
        CheckConstraint(
            f"type IN ('{ExerciseType.FREE.value}', "
            f"'{ExerciseType.MULTIPLE_CHOICE.value}')",
            name="ck_exercise_type_enum",
        ),
        CheckConstraint(
            f"((option_a IS NOT NULL AND option_b IS NOT NULL "
            f"AND type = '{ExerciseType.MULTIPLE_CHOICE.value}') "
            f"OR (answers IS NOT NULL AND type = '{ExerciseType.FREE.value}')) "
            f"AND (answers IS NULL OR (option_a IS NULL AND option_b IS NULL))",
            name="ck_exercise_options_only_for_multiple_choice",
        ),
        nullable=False,
    )
    definition = Column(String(512), nullable=False)
    text = Column(String(2048), nullable=False)
    link = Column(String(512))
    option_a = Column(String)
    option_b = Column(String)
    option_c = Column(String)
    option_d = Column(String)
    answers = Column(
        String(2048),
        CheckConstraint(
            f"answers IS NOT NULL OR type = '{ExerciseType.MULTIPLE_CHOICE.value}'",
            name="ck_exercise_answers_only_for_free",
        ),
    )
