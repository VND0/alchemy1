from flask import Flask
from sqlalchemy.exc import IntegrityError

from data import db_session
from data.users import User

app = Flask(__name__)
app.config["SECRET_KEY"] = "89d5be8d17a5422d76807e1f3f53b2d3"


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


if __name__ == "__main__":
    db_session.global_init("db/data.db")
    try:
        add_people()
    except IntegrityError:
        pass

    # app.run(host="localhost", port=8080, debug=True)
