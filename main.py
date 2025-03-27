from datetime import datetime as dt, timedelta as td, date

from flask import Flask, render_template, redirect, request, abort
from flask_login import LoginManager, login_required, logout_user, current_user, login_user
from flask_restful import Api
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from werkzeug.security import generate_password_hash, check_password_hash

import jobs_api
import users_resource
from data import db_session
from data.db_session import create_session
from data.job import Job, EmptyJob
from data.users import User
from forms.auth import LoginForm
from forms.job import JobForm
from forms.registration import RegistrationForm

app = Flask(__name__)
app.config["SECRET_KEY"] = "89d5be8d17a5422d76807e1f3f53b2d3"
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.register_blueprint(jobs_api.bp)
login_manager = LoginManager()
login_manager.init_app(app)
api = Api(app)
api.add_resource(users_resource.UsersListResource, "/api/v2/users")
api.add_resource(users_resource.UsersResource, "/api/v2/users/<int(signed=True):user_id>")


@login_manager.user_loader
def load_user(user_id: int) -> User | None:
    session = db_session.create_session()
    return session.query(User).filter(User.id == user_id).one_or_none()


def restrict_logged(func):
    def wrapper(*args, **kwargs):
        if current_user.is_authenticated:
            return redirect("/")
        else:
            return func(*args, **kwargs)

    wrapper.__name__ = func.__name__
    return wrapper


def add_people():
    session = db_session.create_session()

    cap = User(surname="Scott", name="Ridley", age=21, position="captain", speciality="research_engineer",
               address="module_1", email="scott_chief@mars.org")
    session.add(cap)

    people = [
        User(surname=f"CrewS{i}", name=f"CrewN{i}", age=21 + i, position="crew", speciality=f"spec{i}",
             address=f"module_{i}", email=f"email{i}@mars.org") for i in range(1, 5)
    ]
    for p in people:
        session.add(p)

    session.commit()


def add_jobs():
    session = db_session.create_session()
    if session.query(Job).first():
        return

    jobs = [
        Job(team_leader=1, work_size=15, collaborators="2, 3", start_date=dt.now(), is_finished=False,
            job="deployment of residential modules 1 and 2", end_date=(dt.now() + td(hours=10)))
    ]
    session.add_all(jobs)
    session.commit()


def handle_registration(form: RegistrationForm) -> str | None:
    try:
        assert form.passwd.data == form.passwd_confirmation.data

        user = User(
            surname=form.surname.data,
            name=form.name.data,
            age=form.age.data,
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data,
            email=form.email.data,
            hashed_password=generate_password_hash(form.passwd.data)
        )
        session = create_session()
        session.add(user)
        session.commit()
        login_user(user, remember=form.remember_me.data)
    except AssertionError:
        return "Passwords are not equal"
    except IntegrityError:
        return "User already exists or some data is malformed"


def handle_authorization(form: LoginForm) -> str | None:
    session = db_session.create_session()
    user = session.query(User).filter(User.email == form.email.data).one_or_none()
    if not user or not check_password_hash(user.hashed_password, form.password.data):
        return "Wrong email or password"
    login_user(user, remember=form.remember_me.data)


@app.route("/register", methods=["POST", "GET"])
@restrict_logged
def register():
    err = None
    form = RegistrationForm()
    if form.validate_on_submit():
        err = handle_registration(form)
        if err is None:
            return redirect("/")

    return render_template("register.html", title="Регистрация", form=form, err=err)


@app.route("/login", methods=["POST", "GET"])
@restrict_logged
def login():
    form = LoginForm()
    err = None
    if form.validate_on_submit():
        err = handle_authorization(form)
        if err is None:
            return redirect("/")

    return render_template("login.html", form=form, title="Авторизация", err=err)


@app.get("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")


def add_job(form: JobForm):
    print(form.work_size.data)
    job = Job(
        team_leader=form.lead_id.data,
        job=form.title.data,
        work_size=form.work_size.data,
        collaborators=form.collab_list.data,
        start_date=date.today(),
        end_date=(dt.now() + td(hours=form.work_size.data)).date(),
        is_finished=form.is_finished.data,
    )
    try:
        session = db_session.create_session()
        session.add(job)
        session.commit()
    except IntegrityError:
        return "An error occurred. Maybe the problem is wrong team leader's id."


@app.route("/new-job", methods=["POST", "GET"])
@login_required
def new_job():
    err = None
    form = JobForm()
    if form.validate_on_submit():
        err = add_job(form)
        if err is None:
            return redirect("/")

    return render_template("add_job.html", title="Adding a job", err=err, form=form, job=EmptyJob())


@app.get("/del-job")
@login_required
def del_job():
    who = current_user.id
    what = request.args.get("which")

    session = db_session.create_session()
    job = session.query(Job).filter(Job.id == what).one_or_none()
    if job is None:
        abort(400)
    if job.team_leader != who and who != 1:
        abort(403)

    session.delete(job)
    session.commit()
    return redirect("/")


def apply_job_changes(form: JobForm, job: Job, session: Session):
    job.job = form.title.data
    job.team_leader = form.lead_id.data
    job.work_size = form.work_size.data
    job.collaborators = form.collab_list.data
    job.is_finished = form.is_finished.data

    session.commit()


@app.route("/edit-job/<int:job_id>", methods=["POST", "GET"])
@login_required
def edit_job(job_id: int):
    session = db_session.create_session()
    job = session.query(Job).filter(Job.id == job_id).one_or_none()
    if not job:
        abort(400)
    if current_user.id not in (job.team_leader, 1):
        abort(403)

    form = JobForm()
    if form.validate_on_submit():
        apply_job_changes(form, job, session)
        return redirect("/")

    return render_template("add_job.html", form=form, job=job)


@app.get("/")
def index():
    session = db_session.create_session()
    jobs = session.query(Job).all()
    return render_template("index.html", jobs=jobs, round=round)


if __name__ == "__main__":
    db_session.global_init("db/data.db")
    try:
        add_people()
    except IntegrityError:
        pass
    add_jobs()
    app.run(host="localhost", port=8080, debug=True)
