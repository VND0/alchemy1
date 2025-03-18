import sqlalchemy as sa
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from .db_session import SqlAlchemyBase


class Department(SqlAlchemyBase):
    __tablename__ = "departments"
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    title = sa.Column(sa.String)
    chief = sa.Column(sa.Integer, ForeignKey("users.id"))
    members = sa.Column(sa.String)
    email = sa.Column(sa.String)

    user = relationship("User")
