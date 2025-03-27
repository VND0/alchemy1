import requests

URL = "http://localhost:8080/api/jobs"
DATA = {
    "job": "test job 1",
    "team_leader": "1",
    "work_size": 1,
    "collaborators": "",
    "is_finished": True
}


def get_all():
    response = requests.get(URL)
    print("LIST OF ALL JOBS")
    print(response.json())


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
    job_id = add_request()
    get_all()
    change_name_ok(job_id)
    get_all()
    change_id_bad(job_id)
    bad_datatype_put(job_id)
    get_all()
