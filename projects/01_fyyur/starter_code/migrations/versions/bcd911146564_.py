"""empty message

Revision ID: bcd911146564
Revises: 1a9bb44fc6f9
Create Date: 2020-07-05 11:31:07.298754

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bcd911146564'
down_revision = '1a9bb44fc6f9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('Artist', 'name',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('Show', 'artist_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('Show', 'start_date',
               existing_type=sa.DATE(),
               nullable=False)
    op.alter_column('Show', 'venue_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.drop_column('Show', 'end_date')
    op.alter_column('Venue', 'name',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.create_unique_constraint(None, 'Venue', ['name'])
    op.create_unique_constraint(None, 'Venue', ['website'])
    op.create_unique_constraint(None, 'Venue', ['facebook_link'])
    op.create_unique_constraint(None, 'Venue', ['phone'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'Venue', type_='unique')
    op.drop_constraint(None, 'Venue', type_='unique')
    op.drop_constraint(None, 'Venue', type_='unique')
    op.drop_constraint(None, 'Venue', type_='unique')
    op.alter_column('Venue', 'name',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.add_column('Show', sa.Column('end_date', sa.DATE(), autoincrement=False, nullable=True))
    op.alter_column('Show', 'venue_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('Show', 'start_date',
               existing_type=sa.DATE(),
               nullable=True)
    op.alter_column('Show', 'artist_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('Artist', 'name',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###