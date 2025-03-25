from flask import jsonify
from flask_restful import Resource, abort

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


class UsersListResource(Resource):
    def get(self):
        session = db_session.create_session()
        users = session.query(User).all()
        print("Hello")
        return jsonify(list(map(User.serialize, users)))
