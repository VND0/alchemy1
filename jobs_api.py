import json
from datetime import datetime as dt, timedelta as td, date
from typing import Any

from flask import Blueprint, jsonify, Response, make_response, request
from sqlalchemy.exc import NoResultFound, IntegrityError
from werkzeug.exceptions import HTTPException

from data import db_session
from data.job import Job

bp = Blueprint(
    "api",
    __name__,
    template_folder="templates",
    url_prefix="/api"
)


@bp.errorhandler(HTTPException)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    # start with the correct headers and status code from the error
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response


def form_error(message: Any, status_code: int = 400) -> Response:
    response = make_response({"status": "error", "message": message}, status_code)
    response.headers["Content-Type"] = "application/json"
    return response


def get_jobs():
    session = db_session.create_session()
    jobs = session.query(Job).all()
    return jsonify([j.serialize() for j in jobs])


def add_job():
    data = request.get_json()
    session = db_session.create_session()
    try:
        new_job = Job(
            job=data["job"],
            team_leader=data["team_leader"],
            work_size=data["work_size"],
            collaborators=data["collaborators"],
            is_finished=data["is_finished"],
            start_date=date.today(),
            end_date=(dt.now() + td(hours=data["work_size"])).date(),
        )
    except KeyError:
        return form_error("Not enough data")
    except TypeError:
        return form_error("Some arguments are malformed")
    try:
        session.add(new_job)
        session.commit()
    except IntegrityError:
        return form_error("Conflict with existing data", 409)
    except Exception as e:
        return form_error(f"{type(e): some arguments are malformed}")
    session.refresh(new_job)
    return jsonify(new_job.serialize())


@bp.route("/jobs", methods=["POST", "GET"])
def handle_jobs():
    if request.method == "GET":
        return get_jobs()
    elif request.method == "POST":
        return add_job()


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
