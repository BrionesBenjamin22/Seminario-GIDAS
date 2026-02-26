"""Move fuente_financiamiento from becario to beca

Revision ID: 6e048ae905a8
Revises: b2c3d4e5f6g7
Create Date: 2026-02-25 22:36:40.591413

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6e048ae905a8'
down_revision = 'b2c3d4e5f6g7'
branch_labels = None
depends_on = None

naming_convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}


def upgrade():
    # 1. Add fuente_financiamiento_id to beca table
    with op.batch_alter_table('beca', schema=None, naming_convention=naming_convention) as batch_op:
        batch_op.add_column(sa.Column('fuente_financiamiento_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(
            'fk_beca_fuente_financiamiento_id_fuente_financiamiento',
            'fuente_financiamiento', ['fuente_financiamiento_id'], ['id']
        )

    # 2. Remove fuente_financiamiento_id from becario table
    with op.batch_alter_table('becario', schema=None, naming_convention=naming_convention) as batch_op:
        batch_op.drop_column('fuente_financiamiento_id')


def downgrade():
    # 1. Re-add fuente_financiamiento_id to becario table
    with op.batch_alter_table('becario', schema=None, naming_convention=naming_convention) as batch_op:
        batch_op.add_column(sa.Column('fuente_financiamiento_id', sa.INTEGER(), nullable=True))
        batch_op.create_foreign_key(
            'fk_becario_fuente_financiamiento_id_fuente_financiamiento',
            'fuente_financiamiento', ['fuente_financiamiento_id'], ['id']
        )

    # 2. Remove fuente_financiamiento_id from beca table
    with op.batch_alter_table('beca', schema=None, naming_convention=naming_convention) as batch_op:
        batch_op.drop_column('fuente_financiamiento_id')
