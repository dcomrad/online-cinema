"""empty message

Revision ID: 99fa9387847b
Revises: 
Create Date: 2023-11-03 22:41:07.048621

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '99fa9387847b'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute("CREATE SCHEMA IF NOT EXISTS billing;")
    op.create_table('provider',
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id'),
    schema='billing'
    )
    op.create_table('subscription',
    sa.Column('name', sa.String(length=120), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('price', sa.SmallInteger(), nullable=False),
    sa.Column('currency', sa.String(length=10), nullable=True),
    sa.Column('recurring_interval', sa.String(length=10), nullable=True),
    sa.Column('recurring_interval_count', sa.SmallInteger(), nullable=False),
    sa.Column('permission_rank', sa.SmallInteger(), nullable=True),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id'),
    schema='billing'
    )
    op.create_table('payment_method',
    sa.Column('type', sa.String(length=10), nullable=True),
    sa.Column('payload', postgresql.JSON(astext_type=sa.Text()), nullable=True),
    sa.Column('is_default', sa.Boolean(), nullable=False),
    sa.Column('provider_id', sa.UUID(), nullable=False),
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('provider_payment_method_id', sa.String(length=64), nullable=False),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.ForeignKeyConstraint(['provider_id'], ['billing.provider.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id'),
    schema='billing'
    )
    op.create_table('user_subscription',
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('subscription_id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text("TIMEZONE('utc', now())"), nullable=True),
    sa.Column('expired_at', sa.Date(), nullable=True),
    sa.Column('auto_renewal', sa.Boolean(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.ForeignKeyConstraint(['subscription_id'], ['billing.subscription.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id'),
    schema='billing'
    )
    op.create_table('transaction',
    sa.Column('provider_id', sa.UUID(), nullable=False),
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('subscription_id', sa.UUID(), nullable=False),
    sa.Column('payment_method_id', sa.UUID(), nullable=False),
    sa.Column('provider_transaction_id', sa.String(length=64), nullable=False),
    sa.Column('amount', sa.SmallInteger(), nullable=False),
    sa.Column('currency', sa.String(length=10), nullable=True),
    sa.Column('status', sa.String(length=40), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text("TIMEZONE('utc', now())"), nullable=True),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.ForeignKeyConstraint(['payment_method_id'], ['billing.payment_method.id'], ),
    sa.ForeignKeyConstraint(['provider_id'], ['billing.provider.id'], ),
    sa.ForeignKeyConstraint(['subscription_id'], ['billing.subscription.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id'),
    schema='billing'
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('transaction', schema='billing')
    op.drop_table('user_subscription', schema='billing')
    op.drop_table('payment_method', schema='billing')
    op.drop_table('subscription', schema='billing')
    op.drop_table('provider', schema='billing')
    op.execute("DROP SCHEMA IF EXISTS billing;")
    # ### end Alembic commands ###