import sqlalchemy as sa

from .db_session import SqlAlchemyBase


class EmptyJob:
    job = None
    team_leader = None
    work_size = None
    collaborators = None
    is_finished = None


class Job(EmptyJob, SqlAlchemyBase):
    __tablename__ = "jobs"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    team_leader = sa.Column(sa.Integer, sa.ForeignKey("users.id"))
    job = sa.Column(sa.String)
    work_size = sa.Column(sa.Integer)
    collaborators = sa.Column(sa.String)
    start_date = sa.Column(sa.Date)
    end_date = sa.Column(sa.Date)
    is_finished = sa.Column(sa.Boolean)
