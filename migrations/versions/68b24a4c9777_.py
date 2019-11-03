"""empty message

Revision ID: 68b24a4c9777
Revises: db4789b3d7d4
Create Date: 2019-11-03 15:25:04.827730

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '68b24a4c9777'
down_revision = 'db4789b3d7d4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('events', sa.Column('notice_days', sa.Integer(), nullable=True))
    op.add_column('events', sa.Column('notice_mult', sa.Float(), nullable=True))
    op.drop_index('ix_events_id', table_name='events')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index('ix_events_id', 'events', ['id'], unique=False)
    op.drop_column('events', 'notice_mult')
    op.drop_column('events', 'notice_days')
    # ### end Alembic commands ###