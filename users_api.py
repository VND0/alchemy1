import json
from re import match

from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import HTTPException
from werkzeug.security import generate_password_hash

from data import db_session
from data.users import User

UserJSON = dict[str, str | int | bool]
bp = Blueprint(
    "users_api",
    __name__,
    url_prefix="/api/users"
)


@bp.errorhandler(HTTPException)
def handle_exception(e):
    response = e.get_response()
    response.data = json.dumps(e.description)
    response.content_type = "application/json"
    return response


def abort(status_code: int, **kwargs):
    err = HTTPException
    err.code = status_code
    err.description = kwargs
    raise err


def get_users():
    session = db_session.create_session()
    users = session.query(User).all()
    return jsonify(list(map(User.serialize, users)))


def create_user():
    session = db_session.create_session()
    body: UserJSON = request.get_json()
    try:

        assert type(body["age"]) is int
        assert match(r"^\S+@\S+\.\S+$", body["email"])
        for v in body.values():
            assert v or v in (0, False)

        user = User(
            surname=body["surname"],
            name=body["name"],
            age=body["age"],
            position=body["position"],
            speciality=body["speciality"],
            address=body["address"],
            email=body["email"],
            hashed_password=generate_password_hash(body["password"])
        )
    except KeyError:
        abort(400, message="Bad JSON keys")
    except AssertionError:
        abort(400, message="Bad email, datatypes or there are some empty fields")

    try:
        session.add(user)
        session.commit()
    except IntegrityError:
        abort(409, message="Given email is busy")

    session.refresh(user)
    return jsonify(user.serialize())


@bp.route("/", methods=["GET", "POST"])
def handle_no_id():
    if request.method == "GET":
        return get_users()
    else:
        return create_user()


def get_user(user_id: int):
    session = db_session.create_session()
    user = session.query(User).filter(User.id == user_id).one_or_none()
    if not user:
        abort(404, message=f"User with ID {user_id} not found")
    session.refresh(user)
    return jsonify(user.serialize())


def edit_user(user_id: int):
    session = db_session.create_session()
    user = session.query(User).filter(User.id == user_id).one_or_none()
    if not user:
        abort(404, message=f"User with ID {user_id} not found")

    body: UserJSON = request.get_json()
    for col in user.__table__.columns:
        attr = col.name
        if attr == "id":
            abort(400, message="Can't edit ID")

        new_value = body.get(attr)
        if not new_value:
            continue
        current_value = getattr(user, attr)
        if type(current_value) is not type(new_value):
            abort(400, message=f"Bad datatype of {attr}")

        setattr(user, attr, new_value)

    try:
        session.commit()
    except IntegrityError:
        abort(409, message="Email must be unique")
    session.refresh(user)

    return jsonify(user.serialize())


def delete_user(user_id: int):
    session = db_session.create_session()
    user = session.query(User).filter(User.id == user_id).one_or_none()
    if not user:
        abort(404, message=f"User with ID {user_id} not found")
    session.delete(user)
    session.commit()
    return jsonify({"status": "deleted"})


@bp.route("/<int(signed=True):user_id>", methods=["GET", "PUT", "DELETE"])
def handle_id(user_id: int):
    if request.method == "GET":
        return get_user(user_id)
    elif request.method == "PUT":
        return edit_user(user_id)
    else:
        return delete_user(user_id)
