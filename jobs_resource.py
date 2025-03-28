from flask import jsonify, make_response
from flask_restful import Resource, abort, reqparse, request

from data import db_session
from data.job import Job

parser = reqparse.RequestParser()

parser.add_argument("job", required=True)
parser.add_argument("team_leader", type=int, required=True)
parser.add_argument("work_size", type=int, required=True)
parser.add_argument("collaborators", required=True)
parser.add_argument("is_finished", type=bool, required=True)


class JobsResource(Resource):
    def get(self, job_id: str):
        try:
            job_id = int(job_id)
        except ValueError:
            abort(400, message="ID has bad datatype")

        session = db_session.create_session()
        job = session.query(Job).filter(Job.id == job_id).one_or_none()
        if job is None:
            abort(404, messsage=f"Job {job_id} not found")
        return jsonify(job.serialize())

    def put(self, job_id: int):
        try:
            job_id = int(job_id)
        except ValueError:
            abort(400, message="ID has bad datatype")

        session = db_session.create_session()
        job = session.query(Job).filter(Job.id == job_id).one_or_none()
        if job is None:
            abort(404, message=f"Job {job_id} not found")

        body = request.get_json()
        if "id" in body:
            abort(400, message="Can't change ID")

        for col in job.__table__.columns:
            attr = col.name
            current_value = getattr(job, attr)
            new_value = body.get(attr)
            if new_value is None:
                continue
            if type(current_value) is not type(new_value):
                abort(400, message=f"{attr} has bad datatype")

            setattr(job, attr, new_value)

        try:
            session.commit()
        except Exception as e:
            abort(409, message=type(e).__name__)

    def delete(self, job_id: int):
        try:
            job_id = int(job_id)
        except ValueError:
            abort(400, message="ID has bad datatype")

        session = db_session.create_session()
        job = session.query(Job).filter(Job.id == job_id).one_or_none()
        if job is None:
            abort(404, message=f"Job {job_id} not found")
        session.delete(job)
        session.commit()
        return make_response("", 204)


class JobsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        jobs = session.query(Job).all()
        return jsonify(list(map(Job.serialize, jobs)))

    def post(self):
        session = db_session.create_session()
        args = parser.parse_args()

        new_job = Job(
            job=args.job,
            team_leader=args.team_leader,
            work_size=args.work_size,
            collaborators=args.collaborators,
            is_finished=args.is_finished
        )
        try:
            session.add(new_job)
            session.commit()
        except Exception as e:
            abort(409, message=type(e).__name__)

        session.refresh(new_job)
        return make_response(jsonify(new_job.serialize()), 201)
