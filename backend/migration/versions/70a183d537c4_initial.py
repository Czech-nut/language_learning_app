"""initial

Revision ID: 70a183d537c4
Revises: 
Create Date: 2022-09-16 10:10:18.000285

"""
from alembic import op
import sqlalchemy as sa

from app.database.models import ExerciseType
import sqlalchemy_utils

# revision identifiers, used by Alembic.
revision = '70a183d537c4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('lesson',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=1024), nullable=False),
    sa.Column('content', sa.String(), nullable=False),
    sa.Column('order', sa.Integer(), nullable=False),
    sa.Column('preview', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_lesson')),
    sa.UniqueConstraint('order', name=op.f('uq_lesson_order'))
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('email', sqlalchemy_utils.types.email.EmailType(length=256), nullable=False),
    sa.Column('background', sqlalchemy_utils.types.color.ColorType(length=20), nullable=False),
    sa.Column('emoji', sa.String(length=24), nullable=False),
    sa.Column('password', sqlalchemy_utils.types.password.PasswordType(max_length=1137), nullable=True),
    sa.Column('streak', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_user'))
    )
    op.create_table('exercise',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('lesson_id', sa.Integer(), nullable=True),
    sa.Column('type', sa.String(), nullable=False),
    sa.Column('definition', sa.String(length=512), nullable=False),
    sa.Column('text', sa.String(length=2048), nullable=False),
    sa.Column('link', sa.String(length=512), nullable=True),
    sa.Column('option_a', sa.String(), nullable=False),
    sa.Column('option_b', sa.String(), nullable=False),
    sa.Column('option_c', sa.String(), nullable=False),
    sa.Column('option_d', sa.String(), nullable=False),
    sa.Column('answers', sa.String(length=2048), nullable=False),
    sa.ForeignKeyConstraint(['lesson_id'], ['lesson.id'], name=op.f('fk_exercise_lesson_id_lesson')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_exercise')),
    sa.CheckConstraint(
        f"(option_a IS NULL AND option_b IS NULL) OR type = '{ExerciseType.MULTIPLE_CHOICE.value}'",
        name="multiple_choice_option"
    ),
    sa.CheckConstraint(
        f"(answers IS NULL) OR type = '{ExerciseType.FREE.value}'",
        name="answers_option"
    ),
    sa.CheckConstraint(
        f"type IN ('{ExerciseType.FREE.value}', "
        f"'{ExerciseType.MULTIPLE_CHOICE.value}')",
        name="type_enum",
    ),
    )

    op.create_table('progress',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('lesson_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['lesson_id'], ['lesson.id'], name=op.f('fk_progress_lesson_id_lesson')),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name=op.f('fk_progress_user_id_user'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_progress'))
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('progress')
    op.drop_table('exercise')
    op.drop_table('user')
    op.drop_table('lesson')
    # ### end Alembic commands ###
