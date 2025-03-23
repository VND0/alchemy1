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

    def serialize(self, exclude: list[str] = None) -> dict[str, Any]:
        if exclude is None:
            exclude = []
        data = {}
        for col in self.__table__.columns:
            attr = col.name
            if attr in exclude:
                continue
            data[attr] = getattr(self, attr)

        return data
