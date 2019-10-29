"""empty message

Revision ID: 759946a0d52c
Revises: 
Create Date: 2019-10-28 15:26:35.960954

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '759946a0d52c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=64), nullable=False),
    sa.Column('surname', sa.String(length=64), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=False),
    sa.Column('email', sa.Text(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('password_hash', sa.String(length=128), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_table('events',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('organised_by', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['organised_by'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_events_id'), 'events', ['id'], unique=False)
    op.create_index(op.f('ix_events_organised_by'), 'events', ['organised_by'], unique=False)
    op.create_table('attendance',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('recorded_at', sa.DateTime(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('event_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['event_id'], ['events.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_attendance_event_id'), 'attendance', ['event_id'], unique=False)
    op.create_index(op.f('ix_attendance_id'), 'attendance', ['id'], unique=False)
    op.create_index(op.f('ix_attendance_user_id'), 'attendance', ['user_id'], unique=False)
    op.create_table('event_events',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('update_created_at', sa.DateTime(), nullable=False),
    sa.Column('is_active_update', sa.Boolean(), nullable=False),
    sa.Column('event_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=False),
    sa.Column('start_at', sa.DateTime(), nullable=False),
    sa.Column('end_at', sa.DateTime(), nullable=False),
    sa.Column('location', sa.String(length=128), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('is_confirmed', sa.Boolean(), nullable=False),
    sa.Column('notice_days', sa.Integer(), nullable=False),
    sa.Column('notice_mult', sa.Float(), nullable=False),
    sa.Column('has_happened', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('organised_by', sa.Integer(), nullable=True),
    sa.Column('attendee_cnt', sa.Integer(), nullable=True),
    sa.Column('attendee_mult', sa.Float(), nullable=True),
    sa.Column('points_pp', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['event_id'], ['events.id'], ),
    sa.ForeignKeyConstraint(['organised_by'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_event_events_event_id'), 'event_events', ['event_id'], unique=False)
    op.create_index(op.f('ix_event_events_id'), 'event_events', ['id'], unique=False)
    op.create_index(op.f('ix_event_events_organised_by'), 'event_events', ['organised_by'], unique=False)
    op.create_table('proposal_responses',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('description', sa.String(length=32), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('event_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['event_id'], ['events.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_proposal_responses_event_id'), 'proposal_responses', ['event_id'], unique=False)
    op.create_index(op.f('ix_proposal_responses_id'), 'proposal_responses', ['id'], unique=False)
    op.create_index(op.f('ix_proposal_responses_user_id'), 'proposal_responses', ['user_id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_proposal_responses_user_id'), table_name='proposal_responses')
    op.drop_index(op.f('ix_proposal_responses_id'), table_name='proposal_responses')
    op.drop_index(op.f('ix_proposal_responses_event_id'), table_name='proposal_responses')
    op.drop_table('proposal_responses')
    op.drop_index(op.f('ix_event_events_organised_by'), table_name='event_events')
    op.drop_index(op.f('ix_event_events_id'), table_name='event_events')
    op.drop_index(op.f('ix_event_events_event_id'), table_name='event_events')
    op.drop_table('event_events')
    op.drop_index(op.f('ix_attendance_user_id'), table_name='attendance')
    op.drop_index(op.f('ix_attendance_id'), table_name='attendance')
    op.drop_index(op.f('ix_attendance_event_id'), table_name='attendance')
    op.drop_table('attendance')
    op.drop_index(op.f('ix_events_organised_by'), table_name='events')
    op.drop_index(op.f('ix_events_id'), table_name='events')
    op.drop_table('events')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_table('users')
    # ### end Alembic commands ###
