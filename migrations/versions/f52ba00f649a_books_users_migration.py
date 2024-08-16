"""books_users_migration

Revision ID: f52ba00f649a
Revises: 
Create Date: 2024-08-15 20:54:42.438114

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy.sql as sql

# revision identifiers, used by Alembic.
revision = 'f52ba00f649a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Create the user table
    op.create_table(
        'user',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(length=250), nullable=False),
        sa.Column('password_hash', sa.String(length=120), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )
    
    # Create the book table
    op.create_table(
        'book',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=120), nullable=False),
        sa.Column('author', sa.String(length=120), nullable=False),
        sa.Column('genre', sa.String(length=80), nullable=False),
        sa.Column('year_published', sa.Integer(), nullable=False),
        sa.Column('summary', sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create the review table
    op.create_table(
        'review',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('book_id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('review_text', sa.Text(), nullable=False),
        sa.Column('rating', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['book_id'], ['book.id']),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'])
    )


def downgrade():
    # Drop the review table
    op.drop_table('review')
    
    # Drop the book table
    op.drop_table('book')
    
    # Drop the user table
    op.drop_table('user')
