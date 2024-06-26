"""Init

Revision ID: 451542604212
Revises: 
Create Date: 2024-05-12 20:42:30.066648

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '451542604212'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('contacts',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('first_name', sa.String(length=50), nullable=False),
    sa.Column('last_name', sa.String(length=50), nullable=False),
    sa.Column('email', sa.String(length=50), nullable=False),
    sa.Column('phone_number', sa.String(length=50), nullable=False),
    sa.Column('birthday', sa.DateTime(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('contacts')
    # ### end Alembic commands ###

def upgrade():
    op.create_table('users', sa.Column('id', sa.Integer(), nullable=False), sa.Column('email', sa.String(length=120), nullable=False), sa.Column('created_at', sa.DateTime(), nullable=False), sa.PrimaryKeyConstraint('id'))
    op.create_table('contacts', sa.Column('id', sa.Integer(), nullable=False), sa.Column('user_id', sa.Integer(), nullable=False), sa.Column('created_at', sa.DateTime(), nullable=False), sa.PrimaryKeyConstraint('id'), sa.ForeignKeyConstraint(['user_id'], ['users.id']))
    op.create_table('contact_requests', sa.Column('id', sa.Integer(), nullable=False), sa.Column('user_id', sa.Integer(), nullable=False), sa.Column('created_at', sa.DateTime(), nullable=False), sa.PrimaryKeyConstraint('id'), sa.ForeignKeyConstraint(['user_id'], ['users.id']))
    op.create_table('contact_limits', sa.Column('id', sa.Integer(), nullable=False), sa.Column('user_id', sa.Integer(), nullable=False), sa.Column('limit', sa.Integer(), nullable=False), sa.Column('created_at', sa.DateTime(), nullable=False), sa.PrimaryKeyConstraint('id'), sa.ForeignKeyConstraint(['user_id'], ['users.id']))

def downgrade():
    op.drop_table('contact_limits')
    op.drop_table('contact_requests')
    op.drop_table('contacts')
    op.drop_table('users')