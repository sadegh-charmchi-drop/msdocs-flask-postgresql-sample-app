"""Initial migration.

Revision ID: d0c7b8e4b57c
Revises: 
Create Date: 2022-11-08 17:00:02.151921

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd0c7b8e4b57c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('saleorder',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('order_number', sa.String(length=50), nullable=True),
    sa.Column('customer', sa.String(length=50), nullable=True),
    sa.Column('order_date', sa.DateTime(), nullable=True),
    sa.Column('total_amount', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('saleorderitem',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('saleorder', sa.Integer(), nullable=True),
    sa.Column('product', sa.String(length=30), nullable=True),
    sa.Column('quantity', sa.Integer(), nullable=True),
    sa.Column('item_description', sa.String(length=500), nullable=True),
    sa.Column('creation_date', sa.DateTime(), nullable=True),
    sa.Column('subtotal', sa.Double(), nullable=True),
    sa.ForeignKeyConstraint(['saleorder'], ['saleorder.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('saleorderitem')
    op.drop_table('saleorder')
    # ### end Alembic commands ###