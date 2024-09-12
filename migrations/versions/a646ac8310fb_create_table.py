"""create table

Revision ID: a646ac8310fb
Revises: 
Create Date: 2024-09-04 17:22:11.781353

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a646ac8310fb'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('levels',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=False),
    sa.Column('order', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('players',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('player_id', sa.String(length=100), nullable=False),
    sa.Column('last_visit', sa.DateTime(), nullable=False),
    sa.Column('first_visit', sa.DateTime(), nullable=False),
    sa.Column('is_daily_visit', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('player_id')
    )
    op.create_table('prizes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('boosts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('type', sa.String(), nullable=False),
    sa.Column('player_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['player_id'], ['players.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('level_prizes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('received', sa.DateTime(), nullable=False),
    sa.Column('level_id', sa.Integer(), nullable=False),
    sa.Column('prize_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['level_id'], ['levels.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['prize_id'], ['prizes.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('player_levels',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('completed', sa.DateTime(), nullable=True),
    sa.Column('is_completed', sa.Boolean(), nullable=False),
    sa.Column('score', sa.Integer(), nullable=False),
    sa.Column('player_id', sa.Integer(), nullable=False),
    sa.Column('level_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['level_id'], ['levels.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['player_id'], ['players.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('player_levels')
    op.drop_table('level_prizes')
    op.drop_table('boosts')
    op.drop_table('prizes')
    op.drop_table('players')
    op.drop_table('levels')
    # ### end Alembic commands ###
