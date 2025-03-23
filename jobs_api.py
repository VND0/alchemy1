from flask import Blueprint, jsonify
from data import db_session
from data.job import Job

bp = Blueprint(
    "api",
    __name__,
    template_folder="templates",
    url_prefix="/api"
)


@bp.get("/jobs")
def get_jobs():
    session = db_session.create_session()
    jobs = session.query(Job).all()
    return jsonify([j.serialize() for j in jobs])
