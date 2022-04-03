"""create posts table

Revision ID: d3ad9abd3e25
Revises: 
Create Date: 2022-03-27 16:52:11.868350

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd3ad9abd3e25'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
        sa.Column("id", sa.Integer, nullable=False),
        sa.Column("first_name", sa.String, nullable=False),
        sa.Column("last_name", sa.String, nullable=False),
        sa.Column("password", sa.String, nullable=False),
        sa.Column("email", sa.Boolean, server_default='TRUE', nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"))

    op.create_table('posts',
        sa.Column("id", sa.Integer, nullable=False),
        sa.Column("title", sa.String, nullable=False),
        sa.Column("content", sa.String, nullable=False),
        sa.Column("published", sa.Boolean, server_default='TRUE', nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("owner_id", sa.Integer, sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.PrimaryKeyConstraint("id"))


    op.create_table('likes',
        sa.Column("user_id", sa.Integer,
                sa.ForeignKey("users.id", ondelete="CASCADE"),
                    primary_key=True),
        sa.Column("post_id", sa.Integer,
                sa.ForeignKey("posts.id", ondelete="CASCADE"),
                    primary_key=True))


def downgrade():
    op.drop_table('users')
    op.drop_table('posts')
    op.drop_table('likes')