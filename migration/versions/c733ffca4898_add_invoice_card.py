"""add invoice_card

Revision ID: c733ffca4898
Revises: 29da8abcb4e6
Create Date: 2022-11-27 18:46:13.510391

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c733ffca4898'
down_revision = '29da8abcb4e6'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('invoice', sa.Column('card_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'invoice', 'cards', ['card_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'invoice', type_='foreignkey')
    op.drop_column('invoice', 'card_id')
    # ### end Alembic commands ###
