import requests
import time

response_first = requests.get('https://playground.learnqa.ru/ajax/api/longtime_job')
time_seconds = response_first.json()['seconds']
job_token = response_first.json()['token']

try:
    response_second = requests.get('https://playground.learnqa.ru/ajax/api/longtime_job', params={'token': job_token})
    print(f"First response: {response_second.json()['status']}")
    assert 'Job is NOT ready' == response_second.json()['status'], "Wrong job status"

    time.sleep(time_seconds)
    response_third = requests.get('https://playground.learnqa.ru/ajax/api/longtime_job', params={'token': job_token})
    print(f"Third response status: {response_third.json()['status']}")
    print(f"Third response result: {response_third.json()['result']}")
    assert 'Job is ready' == response_third.json()['status'], "Wrong job status. Job is not ready."
    assert None != response_third.json()['result'], "Wrong result"
except:
    print("Wrong request!")
