import requests

URL = "http://localhost:8080/api/users"
BODY = {
    "surname": "S",
    "name": "N",
    "age": -1,
    "position": "P",
    "speciality": "S",
    "address": "A",
    "email": "E@m@a.il",
    "password": "123456"
}


def get_by_invalid_id():
    print("TRYING TO GET USER WITH ID -1")
    response = requests.get(URL + "/-1")
    print(f"{response.status_code=}")
    print(response.json())


def create_ok_and_get() -> int:
    print("TRYING TO CREATE VALID USER")
    response = requests.post(URL, json=BODY)
    user_id = response.json()["id"]
    print(f"{response.status_code=}")
    print(response.json())
    print("TRYING TO GET CREATED USER")
    response = requests.get(URL + f"/{user_id}")
    print(f"{response.status_code=}")
    print(response.json())
    return user_id


def get_all():
    print("TRYING TO GET ALL USERS")
    response = requests.get(URL)
    print(f"{response.status_code=}")
    print(response.json())


def delete_ok(user_id: int):
    print(f"TRYING TO DELETE CREATED USER WITH ID {user_id}")
    response = requests.delete(URL + f"/{user_id}")
    print(f"{response.status_code=}")
    print(response.json())


def delete_by_invalid_id():
    print("TRYING TO DELETE USER WITH ID -1")
    response = requests.delete(URL + "/-1")
    print(f"{response.status_code=}")
    print(response.content)


def create_no_body():
    print("TRYING TO SEND CREATION REQUEST WITH NO BODY")
    response = requests.post(URL)
    print(f"{response.status_code=}")
    print(response.json())


def create_not_enough_data():
    print("TRYING TO CREATE USER WITHOUT SENDING EMAIL")
    body = BODY.copy()
    del body["email"]
    response = requests.post(URL, json=body)
    print(f"{response.status_code=}")
    print(response.json())


def create_with_the_same_email():
    print("TRYING TO CREATE USER WITH BUSY EMAIL")
    response = requests.post(URL, json=BODY)
    print(f"{response.status_code=}")
    print(response.json())


if __name__ == '__main__':
    get_by_invalid_id()
    user_id = create_ok_and_get()
    get_all()
    delete_by_invalid_id()
    create_no_body()
    create_not_enough_data()
    create_with_the_same_email()
    delete_ok(user_id)
