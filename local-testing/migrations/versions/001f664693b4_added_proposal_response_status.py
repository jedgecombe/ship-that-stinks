"""added proposal response status

Revision ID: 001f664693b4
Revises: 5985ed3ce25c
Create Date: 2019-08-16 11:22:59.037719

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '001f664693b4'
down_revision = '5985ed3ce25c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('proposal_response', sa.Column('response_status', sa.String(length=32), nullable=True))
    op.create_index(op.f('ix_proposal_response_response_status'), 'proposal_response', ['response_status'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_proposal_response_response_status'), table_name='proposal_response')
    op.drop_column('proposal_response', 'response_status')
    # ### end Alembic commands ###