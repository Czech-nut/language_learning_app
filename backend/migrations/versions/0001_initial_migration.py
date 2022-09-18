"""Initial migration

Revision ID: 0001
Revises:
Create Date: 2022-09-16 15:09:48.102315

"""
import sqlalchemy as sa
from alembic import op

from app.dtos.exercise import ExerciseType

# revision identifiers, used by Alembic.
revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("CREATE SCHEMA IF NOT EXISTS lla;")
    op.create_table(
        "lesson",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(length=1024), nullable=False),
        sa.Column("content", sa.String(), nullable=False),
        sa.Column("order", sa.Integer(), nullable=False, autoincrement=True),
        sa.Column("preview", sa.String(), nullable=False),
        sa.Column("approved", sa.Boolean(), server_default="false", nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_lesson")),
        sa.UniqueConstraint("order", name=op.f("uq_lesson_order")),
    )
    op.create_table(
        "user",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("email", sa.String(length=256), nullable=False),
        sa.Column("is_admin", sa.Boolean(), server_default="false", nullable=False),
        sa.Column("background", sa.String(length=7), nullable=False),
        sa.Column("emoji", sa.String(length=24), nullable=False),
        sa.Column("password", sa.String(length=256), nullable=False),
        sa.Column("streak", sa.Integer(), server_default="0", nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_user")),
    )
    op.create_table(
        "exercise",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("lesson_id", sa.Integer(), nullable=True),
        sa.Column("type", sa.String(length=128), nullable=False),
        sa.Column("definition", sa.String(length=512), nullable=False),
        sa.Column("text", sa.String(length=2048), nullable=False),
        sa.Column("link", sa.String(length=512), nullable=True),
        sa.Column("option_a", sa.String(), nullable=True),
        sa.Column("option_b", sa.String(), nullable=True),
        sa.Column("option_c", sa.String(), nullable=True),
        sa.Column("option_d", sa.String(), nullable=True),
        sa.Column("answers", sa.String(length=2048), nullable=True),
        sa.ForeignKeyConstraint(
            ["lesson_id"],
            ["lesson.id"],
            name=op.f("fk_exercise_lesson_id_lesson"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_exercise")),
        sa.CheckConstraint(
            f"type IN ('{ExerciseType.FREE.value}', "
            f"'{ExerciseType.MULTIPLE_CHOICE.value}')",
            name="type_enum",
        ),
        sa.CheckConstraint(
            f"((option_a IS NOT NULL AND option_b IS NOT NULL "
            f"AND type = '{ExerciseType.MULTIPLE_CHOICE.value}') "
            f"OR (answers IS NOT NULL AND type = '{ExerciseType.FREE.value}')) "
            f"AND (answers IS NULL OR (option_a IS NULL AND option_b IS NULL))",
            name="options_only_for_multiple_choice",
        ),
    )
    op.create_table(
        "progress",
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("lesson_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["lesson_id"],
            ["lesson.id"],
            name=op.f("fk_progress_lesson_id_lesson"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["user.id"],
            name=op.f("fk_progress_user_id_user"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("user_id", name=op.f("pk_progress")),
    )


def downgrade() -> None:
    op.drop_table("progress")
    op.drop_table("exercise")
    op.drop_table("user")
    op.drop_table("lesson")
