"""create tables

Revision ID: 977cc8d9864e
Revises:
Create Date: 2023-11-01 19:51:35.038702

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '977cc8d9864e'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'provider',
        sa.Column('name', sa.String(length=50), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text("TIMEZONE('utc', now())"), nullable=True),
        sa.Column('id', sa.UUID(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('id')
    )
    op.create_table(
        'subscription',
        sa.Column('name', sa.String(length=120), nullable=False),
        sa.Column('price', sa.SmallInteger(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('recurring_interval', sa.String(length=10), nullable=False),
        sa.Column('recurring_interval_count', sa.SmallInteger(), nullable=False),
        sa.Column('permission_rank', sa.SmallInteger(), nullable=True),
        sa.Column('currency', sa.String(length=10), nullable=False),
        sa.Column('id', sa.UUID(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('id')
    )
    op.create_table(
        'user_subscription',
        sa.Column('user_id', sa.UUID(), nullable=False),
        sa.Column('subscription_id', sa.UUID(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text("TIMEZONE('utc', now())"), nullable=True),
        sa.Column('expired_at', sa.Date(), nullable=True),
        sa.Column('auto_renewal', sa.Boolean(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(['subscription_id'], ['subscription.id'], ),
        sa.PrimaryKeyConstraint('user_id'),
        sa.UniqueConstraint('user_id')
    )
    op.create_table(
        'transaction',
        sa.Column('provider_id', sa.UUID(), nullable=False),
        sa.Column('idempotency_key', sa.UUID(), nullable=False),
        sa.Column('user_id', sa.UUID(), nullable=True),
        sa.Column('amount', sa.SmallInteger(), nullable=False),
        sa.Column('subscription_id', sa.UUID(), nullable=True),
        sa.Column('status', sa.String(length=40), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text("TIMEZONE('utc', now())"), nullable=True),
        sa.Column('id', sa.UUID(), nullable=False),
        sa.ForeignKeyConstraint(['provider_id'], ['provider.id'], ),
        sa.ForeignKeyConstraint(['subscription_id'], ['subscription.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['user_subscription.user_id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('transaction')
    op.drop_table('user_subscription')
    op.drop_table('subscription')
    op.drop_table('provider')
    # ### end Alembic commands ###