import requests

URL = "http://localhost:8080/api/v2/jobs"
DATA = {
    "job": "test job 1",
    "team_leader": 1,
    "work_size": 1,
    "collaborators": "",
    "is_finished": True
}


# Creating
def good_request():
    response = requests.post(URL, json=DATA)
    print("TRYING TO ADD VALID JOB")
    print(f"STATUS CODE {response.status_code}")
    print(response.json())


def bad_arguments1():
    data = DATA.copy()
    del data["job"]  # Deleting parameter causes error
    response = requests.post(URL, json=data)
    print("TRYING TO ADD JOB WITHOUT ACTUALLY JOB")
    print(f"STATUS CODE {response.status_code}")
    print(response.json())


def bad_arguments2():
    data = DATA.copy()
    data["work_size"] = "1"  # Bad argument's data type
    response = requests.post(URL, json=data)
    print("TRYING TO ADD JOB WITH INVALID WORK_SIZE")
    print(f"STATUS CODE {response.status_code}")
    print(response.json())


def no_json():
    response = requests.post(URL)
    print("SENDING POST WITH NO BODY")
    print(f"STATUS CODE {response.status_code}")
    print(response.json())


# Getting
def all_jobs():
    response = requests.get(URL)
    print("GETTING ALL JOBS")
    print(f"STATUS CODE: {response.status_code}")
    print(response.json())


def one_job():
    response = requests.get(URL + "/1")
    print("GETTING JOB WITH ID 1")
    print(f"STATUS CODE: {response.status_code}")
    print(response.json())


def bad_id():
    response = requests.get(URL + "/-1")
    print("GETTING JOB WITH BAD ID -1")
    print(f"STATUS CODE: {response.status_code}")
    print(response.json())


def bad_argument():
    response = requests.get(URL + "/string")
    print("GETTING JOB WITH BAD ID ARGUMENT: string")
    print(f"STATUS CODE: {response.status_code}")
    print(response.json())


# Deleting
def add_valid_and_get_id() -> int:
    print("ADDING VALID JOB")
    response = requests.post(URL, json=DATA).json()
    job_id = response["id"]
    print(f"ID: {job_id}")
    return job_id


def valid_deletion():
    job_id = add_valid_and_get_id()

    all_jobs()
    print("DELETING BY VALID ID")
    response = requests.delete(URL + f"/{job_id}")
    print(f"STATUS CODE {response.status_code}")
    print(response.content)
    all_jobs()


def rm_bad_id():
    print("DELETING BY BAD ID -1")
    response = requests.delete(URL + f"/-1")
    print(f"STATUS CODE {response.status_code}")
    print(response.json())


def bad_datatype():
    print("DELETING BY BAD ID string")
    response = requests.delete(URL + f"/string")
    print(f"STATUS CODE {response.status_code}")
    print(response.json())


# Changing
def add_request() -> int:
    response = requests.post(URL, json=DATA)
    print("TRYING TO ADD VALID JOB")
    print(f"STATUS CODE {response.status_code}")
    json = response.json()
    print(json)
    return json["id"]


def change_name_ok(job_id: int):
    response = requests.put(URL + f"/{job_id}", json={"job": "test job changed"})
    print(f"TRYING TO MODIFY JOB WITH ID {job_id}")
    print(f"STATUS CODE {response.status_code}")
    print(response.json())


def change_id_bad(job_id: int):
    response = requests.put(URL + f"/{job_id}", json={"id": -1})
    print(f"TRYING TO CHANGE ID FOR JOB WITH ID {job_id}")
    print(f"STATUS CODE {response.status_code}")
    print(response.json())


def bad_datatype_put(job_id: int):
    response = requests.put(URL + f"/{job_id}", json={"work_size": "string"})
    print(f"TRYING TO REPLACE WORK SIZE WITH STRING VALUE FOR JOB WITH ID {job_id}")
    print(f"STATUS CODE {response.status_code}")
    print(response.json())


if __name__ == '__main__':
    good_request()
    bad_arguments1()
    bad_arguments2()
    no_json()

    all_jobs()
    one_job()
    bad_id()
    bad_argument()

    valid_deletion()
    rm_bad_id()
    bad_datatype()

    job_id = add_request()
    change_name_ok(job_id)
    change_id_bad(job_id)
    bad_datatype_put(job_id)
