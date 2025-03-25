import pprint

import requests

URL = "http://localhost:8080/api/jobs"


def all_jobs():
    response = requests.get(URL)
    print("GETTING ALL JOBS")
    print(f"STATUS CODE: {response.status_code}")
    pprint.pp(response.json())


def one_job():
    response = requests.get(URL + "/1")
    print("GETTING JOB WITH ID 1")
    print(f"STATUS CODE: {response.status_code}")
    pprint.pp(response.json())


def bad_id():
    response = requests.get(URL + "/-1")
    print("GETTING JOB WITH BAD ID -1")
    print(f"STATUS CODE: {response.status_code}")
    pprint.pp(response.json())


def bad_argument():
    response = requests.get(URL + "/string")
    print("GETTING JOB WITH BAD ID ARGUMENT: string")
    print(f"STATUS CODE: {response.status_code}")
    pprint.pp(response.json())


if __name__ == '__main__':
    all_jobs()
    one_job()
    bad_id()
    bad_argument()
