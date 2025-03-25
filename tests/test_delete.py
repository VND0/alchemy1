import pprint

import requests

import test_create

URL = "http://localhost:8080/api/jobs"


def add_valid_and_get_id() -> int:
    print("ADDING VALID JOB")
    response = requests.post(URL, json=test_create.DATA).json()
    job_id = response["id"]
    print(f"ID: {job_id}")
    return job_id


def valid_deletion():
    job_id = add_valid_and_get_id()
    print("DELETING BY VALID ID")
    response = requests.delete(URL + f"/{job_id}")
    print(f"STATUS CODE {response.status_code}")
    pprint.pp(response.json())


def bad_id():
    print("DELETING BY BAD ID -1")
    response = requests.delete(URL + f"/-1")
    print(f"STATUS CODE {response.status_code}")
    pprint.pp(response.json())


if __name__ == '__main__':
    valid_deletion()
    bad_id()
