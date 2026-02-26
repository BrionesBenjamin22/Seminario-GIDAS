"""Auditoria agregada al personal

Revision ID: 08f38e81daf2
Revises: b3f2e396589a
Create Date: 2026-02-26 02:25:11.093034

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '08f38e81daf2'
down_revision = 'b3f2e396589a'
branch_labels = None
depends_on = None


def upgrade():

    with op.batch_alter_table('becario', schema=None) as batch_op:
        batch_op.add_column(sa.Column('created_at', sa.DateTime(), nullable=False))
        batch_op.add_column(sa.Column('deleted_at', sa.DateTime(), nullable=True))
        batch_op.add_column(sa.Column('created_by', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('deleted_by', sa.Integer(), nullable=True))

        batch_op.create_foreign_key(
            "fk_becario_created_by",
            'usuario',
            ['created_by'],
            ['id']
        )
        batch_op.create_foreign_key(
            "fk_becario_deleted_by",
            'usuario',
            ['deleted_by'],
            ['id']
        )


    with op.batch_alter_table('investigador', schema=None) as batch_op:
        batch_op.add_column(sa.Column('created_at', sa.DateTime(), nullable=False))
        batch_op.add_column(sa.Column('deleted_at', sa.DateTime(), nullable=True))
        batch_op.add_column(sa.Column('created_by', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('deleted_by', sa.Integer(), nullable=True))

        batch_op.create_foreign_key(
            "fk_investigador_created_by",
            'usuario',
            ['created_by'],
            ['id']
        )
        batch_op.create_foreign_key(
            "fk_investigador_deleted_by",
            'usuario',
            ['deleted_by'],
            ['id']
        )


    with op.batch_alter_table('personal', schema=None) as batch_op:
        batch_op.add_column(sa.Column('created_at', sa.DateTime(), nullable=False))
        batch_op.add_column(sa.Column('deleted_at', sa.DateTime(), nullable=True))
        batch_op.add_column(sa.Column('created_by', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('deleted_by', sa.Integer(), nullable=True))

        batch_op.create_foreign_key(
            "fk_personal_created_by",
            'usuario',
            ['created_by'],
            ['id']
        )
        batch_op.create_foreign_key(
            "fk_personal_deleted_by",
            'usuario',
            ['deleted_by'],
            ['id']
        )

def downgrade():

    with op.batch_alter_table('personal', schema=None) as batch_op:
        batch_op.drop_constraint("fk_personal_created_by", type_='foreignkey')
        batch_op.drop_constraint("fk_personal_deleted_by", type_='foreignkey')
        batch_op.drop_column('deleted_by')
        batch_op.drop_column('created_by')
        batch_op.drop_column('deleted_at')
        batch_op.drop_column('created_at')


    with op.batch_alter_table('investigador', schema=None) as batch_op:
        batch_op.drop_constraint("fk_investigador_created_by", type_='foreignkey')
        batch_op.drop_constraint("fk_investigador_deleted_by", type_='foreignkey')
        batch_op.drop_column('deleted_by')
        batch_op.drop_column('created_by')
        batch_op.drop_column('deleted_at')
        batch_op.drop_column('created_at')


    with op.batch_alter_table('becario', schema=None) as batch_op:
        batch_op.drop_constraint("fk_becario_created_by", type_='foreignkey')
        batch_op.drop_constraint("fk_becario_deleted_by", type_='foreignkey')
        batch_op.drop_column('deleted_by')
        batch_op.drop_column('created_by')
        batch_op.drop_column('deleted_at')
        batch_op.drop_column('created_at')
    # ### end Alembic commands ###
