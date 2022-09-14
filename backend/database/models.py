import enum
from sqlalchemy import Column, ForeignKey, Integer, String, Enum
from sqlalchemy_utils import EmailType, ColorType, PasswordType

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(1024))
    email = Column(EmailType(256))
    background_color = Column(ColorType)
    emoji = Column(String(24))
    password = Column(PasswordType(
        schemes=[
            'pbkdf2_sha512',
            'md5_crypt'
        ],

        deprecated=['md5_crypt']
    ))

    streak = Column(Integer)

class Lesson(Base):
    __tablename__ = "lesson"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(1024))
    content = Column(String)
    order = Column('0', unique=True)
    preview = Column(String)


class Progress(Base):
    __tablename__ = "progress"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    lesson_id = Column(Integer, ForeignKey('lesson.id'))


class Exercise(Base):
    __tablename__ = "excercise"

    id = Column(Integer, primary_key=True, index=True)
    lesson_id = Column(Integer, ForeignKey('lesson.id'))
    type = Column(Enum('option_a', 'option_b', 'option_c', 'option_d', name='answer_types'))
    definition = Column(String(512))
    text = Column(String(2048))
    link = Column(String(512), optional=True)
    answer = Column(String(2048))

