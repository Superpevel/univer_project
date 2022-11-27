"""add invoice 1

Revision ID: 29da8abcb4e6
Revises: 356127333156
Create Date: 2022-11-27 18:41:43.300193

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '29da8abcb4e6'
down_revision = '356127333156'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('invoice',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('amount', sa.Float(), nullable=False),
    sa.Column('price', sa.Float(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_invoice_id'), 'invoice', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_invoice_id'), table_name='invoice')
    op.drop_table('invoice')
    # ### end Alembic commands ###
