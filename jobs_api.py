from typing import Any

from flask import Blueprint, jsonify, Response, make_response
from sqlalchemy.exc import NoResultFound

from data import db_session
from data.job import Job

bp = Blueprint(
    "api",
    __name__,
    template_folder="templates",
    url_prefix="/api"
)


def form_error(message: Any, status_code: int = 400) -> Response:
    return make_response({"status": "error", "message": message}, status_code)


@bp.get("/jobs")
def get_jobs():
    session = db_session.create_session()
    jobs = session.query(Job).all()
    return jsonify([j.serialize() for j in jobs])


@bp.get("/jobs/<job_id>")
def get_job(job_id):
    session = db_session.create_session()
    try:
        job = session.query(Job).filter(Job.id == int(job_id)).one()
    except ValueError:
        return form_error("Id is not an integer")
    except NoResultFound:
        return form_error("Couldn't find job with this id")

    return jsonify(job.serialize())
