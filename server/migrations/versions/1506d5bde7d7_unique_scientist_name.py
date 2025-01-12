"""unique scientist name

Revision ID: 1506d5bde7d7
Revises: f8d68f5dc867
Create Date: 2023-03-19 12:27:02.550822

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1506d5bde7d7'
down_revision = 'f8d68f5dc867'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('scientists', schema=None) as batch_op:
        batch_op.create_unique_constraint(None, ['name'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('scientists', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')

    # ### end Alembic commands ###
