import sqlalchemy as sa
from flask_login import UserMixin
from sqlalchemy.orm import relationship

from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = "users"
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    surname = sa.Column(sa.String)
    name = sa.Column(sa.String)
    age = sa.Column(sa.Integer)
    position = sa.Column(sa.String)
    speciality = sa.Column(sa.String)
    address = sa.Column(sa.String)
    email = sa.Column(sa.String, unique=True)
    hashed_password = sa.Column(sa.String)
    modified_date = sa.Column(sa.DateTime)

    departments = relationship("Department", back_populates="user")

    def __repr__(self):
        return f"<Colonist> {self.id} {self.surname} {self.name}"

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
