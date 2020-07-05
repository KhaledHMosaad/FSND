"""empty message

Revision ID: 0147d0acc715
Revises: 752e862c3b94
Create Date: 2020-07-04 21:57:48.000645

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0147d0acc715'
down_revision = '752e862c3b94'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('Venue', 'location_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('Venue', 'location_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###
