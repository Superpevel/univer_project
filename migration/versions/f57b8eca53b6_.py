"""empty message

Revision ID: f57b8eca53b6
Revises: 1e74bc7464c9
Create Date: 2022-10-12 22:05:05.074256

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f57b8eca53b6'
down_revision = '1e74bc7464c9'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'useless')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('useless', sa.VARCHAR(length=500), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
