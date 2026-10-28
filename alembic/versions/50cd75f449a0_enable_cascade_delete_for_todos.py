"""enable cascade delete for todos

Revision ID: 50cd75f449a0
Revises: e0d11b565c9a
Create Date: 2026-10-25 15:16:41.499224

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '50cd75f449a0'
down_revision: Union[str, Sequence[str], None] = 'e0d11b565c9a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    naming_convention = {
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s"
    }

    with op.batch_alter_table(
        "todos",
        naming_convention=naming_convention
    ) as batch_op:
        batch_op.drop_constraint(
            "fk_todos_user_id_users",
            type_="foreignkey"
        )
        batch_op.create_foreign_key(
            "fk_todos_user_id_users",
            "users",
            ["user_id"],
            ["id"],
            ondelete="CASCADE"
        )


def downgrade() -> None:
    with op.batch_alter_table("todos") as batch_op:
        batch_op.drop_constraint(
            "fk_todos_user_id_users",
            type_="foreignkey"
        )
        batch_op.create_foreign_key(
            "fk_todos_user_id_users",
            "users",
            ["user_id"],
            ["id"]
        )
