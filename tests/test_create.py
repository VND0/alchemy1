import pprint
from http.client import responses

import requests

URL = "http://localhost:8080/api/jobs"
DATA = {
    "job": "test job 1",
    "team_leader": "1",
    "work_size": 1,
    "collaborators": "",
    "is_finished": True
}


def good_request():
    response = requests.post(URL, json=DATA)
    print("TRYING TO ADD VALID JOB")
    print(f"STATUS CODE {response.status_code}")
    pprint.pp(response.json())


def bad_arguments1():
    data = DATA.copy()
    del data["job"]  # Deleting parameter causes error
    response = requests.post(URL, json=data)
    print("TRYING TO ADD JOB WITHOUT ACTUALLY JOB")
    print(f"STATUS CODE {response.status_code}")
    pprint.pp(response.json())


def bad_arguments2():
    data = DATA.copy()
    data["work_size"] = "1"  # Bad argument's data type
    response = requests.post(URL, json=data)
    print("TRYING TO ADD JOB WITH INVALID WORK_SIZE")
    print(f"STATUS CODE {response.status_code}")
    pprint.pp(response.json())


def no_json():
    response = requests.post(URL)
    print("SENDING POST WITH NO BODY")
    print(f"STATUS CODE {response.status_code}")
    pprint.pp(response.json())


if __name__ == '__main__':
    good_request()
    bad_arguments1()
    bad_arguments2()
    no_json()
