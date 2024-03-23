import requests
import json
import csv
import os
import time

def poll_ocr_table_job(job_id: str, max_poll_count = 10, poll_interval_sec = 5) -> dict:
    """
    Poll asynchronous job every `poll_interval_sec` seconds
    Raises Exception if job still not finished after `max_poll_count`
    """
    headers = {"Authorization": "Bearer api_key"}
    url = "https://api.edenai.run/v2/ocr/ocr_tables_async"

    for i in range(max_poll_count):
        time.sleep(poll_interval_sec)
        response = requests.get(f"{url}/{job_id}", headers=headers)
        data = response.json()
        if data['status'] == 'finished':
            return data
    raise Exception("Call took too long.")


def microsoft_ocr():
    headers = {"Authorization": "Bearer api_key"}

    file_path = r"Untitled Folder\9.jpg"

    url = "https://api.edenai.run/v2/ocr/ocr_tables_async"
    data = {
        "providers": "microsoft,google",
        'language': 'en'
    }

    files = {'file': open(file_path, 'rb')}

    response = requests.post(url, data=data, files=files, headers=headers)
    result = json.loads(response.text)

    job_id = result['public_id']

    poll_response = poll_ocr_table_job(job_id)
    json_table = poll_response['results']["microsoft"]['pages'][0]['tables'][0]

    csv_table = []
    for row in json_table['rows']:
        csv_row = []
        for cell in row['cells']:
            csv_row.append(cell['text'])
        csv_table.append(csv_row)

    file_name = os.path.basename(file_path)

    with open(f"{file_name}.csv", 'w', newline='') as csvfile:
        tablewriter = csv.writer(csvfile)
        tablewriter.writerows(csv_table)
        print("CSV saved succesfully.")

microsoft_ocr()