import sqlalchemy as sa

from .db_session import SqlAlchemyBase

association_table = sa.Table(
    "association",
    SqlAlchemyBase.metadata,
    sa.Column("jobs", sa.Integer, sa.ForeignKey("jobs.id")),
    sa.Column("categories", sa.Integer, sa.ForeignKey("categories.id"))
)
