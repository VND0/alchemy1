from datetime import date

from flask import jsonify
from flask_restful import Resource, abort, reqparse
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash

from data import db_session
from data.users import User


def abort_if_user_not_found(user_id: int) -> None:
    session = db_session.create_session()
    if not session.query(User).filter(User.id == user_id).one_or_none():
        abort(404, message=f"User {user_id} not found.")


class UsersResource(Resource):
    def get(self, user_id: int):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).filter(User.id == user_id).one()
        return jsonify(user.serialize())

    def put(self, user_id: int):
        abort_if_user_not_found(user_id)

        parser = reqparse.RequestParser()
        parser.add_argument("surname", required=False)
        parser.add_argument("name", required=False)
        parser.add_argument("age", required=False, type=int)
        parser.add_argument("position", required=False)
        parser.add_argument("speciality", required=False)
        parser.add_argument("address", required=False)
        parser.add_argument("email", required=False)
        parser.add_argument("password", required=False)
        args = parser.parse_args()

        session = db_session.create_session()
        user = session.query(User).filter(User.id == user_id).one()
        for col in user.__table__.columns:
            attr = col.name
            if attr == "id":
                continue

            new_value = getattr(args, attr, None)
            if new_value is not None:
                setattr(user, attr, new_value)

        try:
            session.commit()
        except IntegrityError:
            abort(409, message="Email must be unique")
        session.refresh(user)

        return jsonify(user.serialize())

    def delete(self, user_id: int):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        session.query(User).filter(User.id == user_id).delete()
        session.commit()
        return "Ok"


class UsersListResource(Resource):
    def get(self):
        session = db_session.create_session()
        users = session.query(User).all()
        return jsonify(list(map(User.serialize, users)))

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("surname", required=True)
        parser.add_argument("name", required=True)
        parser.add_argument("age", required=True, type=int)
        parser.add_argument("position", required=True)
        parser.add_argument("speciality", required=True)
        parser.add_argument("address", required=True)
        parser.add_argument("email", required=True)
        parser.add_argument("password", required=True)
        args = parser.parse_args()

        session = db_session.create_session()
        new_user = User(
            surname=args.surname,
            name=args.name,
            age=args.age,
            position=args.position,
            speciality=args.speciality,
            address=args.address,
            email=args.email,
            hashed_password=generate_password_hash(args.password),
            modified_date=date.today()
        )
        session.add(new_user)
        try:
            session.commit()
        except IntegrityError:
            abort(409, message="Email must be unique")
        session.refresh(new_user)
        return jsonify(new_user.serialize())
