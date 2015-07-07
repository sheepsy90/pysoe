# -*- coding:utf-8 -*-
import json
import random
import uuid
import os
import requests
import time


def write_data_to_tmp(data_as_list):
    # Create a random name for the data file and make sure it is unique
    tmp_filename = "/tmp/{}.data".format(uuid.uuid4())
    while os.path.exists(tmp_filename):
        tmp_filename = uuid.uuid4()

    file_content = "\n".join([",".join([str(e) for e in element]) for element in data_as_list])

    with open(tmp_filename, "a") as f:
        f.write(file_content)

    return tmp_filename


file_path = write_data_to_tmp([(random.randint(1, 10),
                                random.randint(1, 10),
                                random.randint(1, 10),
                                random.randint(1, 10)) for i in range(100)])

parameters = {
    "comparison_file": file_path,
    "object_count": 10
}

response = requests.post("http://127.0.0.1:5000/soe/schedule",
                         data=json.dumps(parameters),
                         headers={'Content-Type': 'application/json'})

assert response.status_code == 202
assert response.json is not None

job_id = response.json()['job_id']


for cnt in range(20):
    r = requests.get("http://127.0.0.1:5000/soe/schedule_state/{}".format(job_id))
    print(r, r.text)
    time.sleep(0.5)