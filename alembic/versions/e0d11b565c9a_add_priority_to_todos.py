"""add priority to todos

Revision ID: e0d11b565c9a
Revises: 9733895d15d3
Create Date: 2026-10-25 15:11:00.249916

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e0d11b565c9a'
down_revision: Union[str, Sequence[str], None] = '9733895d15d3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "todos",
        sa.Column("priority", sa.String(), nullable=True)
    )


def downgrade() -> None:
    op.drop_column("todos", "priority")
    # ### end Alembic commands ###
