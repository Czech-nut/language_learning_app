import enum
from sqlalchemy import Column, ForeignKey, Integer, String, Enum, column, CheckConstraint, MetaData
from sqlalchemy_utils import EmailType, ColorType, PasswordType

from sqlalchemy.ext.declarative import declarative_base

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
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(EmailType(256), nullable=False)
    background = Column(ColorType, nullable=False)
    emoji = Column(String(24), nullable=False)
    password = Column(PasswordType(
        schemes=[
            'pbkdf2_sha512',
            'md5_crypt'
        ],

        deprecated=['md5_crypt']
    ))

    streak = Column(Integer, nullable=False)


class Lesson(Base):
    __tablename__ = 'lesson'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(1024), nullable=False)
    content = Column(String, nullable=False)
    order = Column(Integer, unique=True, nullable=False)
    preview = Column(String, nullable=False)


class Progress(Base):
    __tablename__ = 'progress'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey(User.id, ondelete="CASCADE"))
    lesson_id = Column(Integer, ForeignKey(Lesson.id))


class ExerciseType(enum.Enum):
    FREE = "free"
    MULTIPLE_CHOICE = "multiple_choice"


class Exercise(Base):
    __tablename__ = 'exercise'

    id = Column(Integer, primary_key=True, autoincrement=True)
    lesson_id = Column(Integer, ForeignKey(Lesson.id))
    type = Column(String, nullable=False)
    definition = Column(String(512), nullable=False)
    text = Column(String(2048), nullable=False)
    link = Column(String(512))
    option_a = Column(String, nullable=False)
    option_b = Column(String, nullable=False)
    option_c = Column(String, nullable=False)
    option_d = Column(String, nullable=False)
    answers = Column(String(2048), nullable=False)
