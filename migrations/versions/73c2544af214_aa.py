"""aa

Revision ID: 73c2544af214
Revises: 0c3f9f31d7e2
Create Date: 2018-05-23 11:12:43.782469

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '73c2544af214'
down_revision = '0c3f9f31d7e2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('confirmed', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'confirmed')
    # ### end Alembic commands ###
