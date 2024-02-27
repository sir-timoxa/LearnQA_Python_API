import requests
import json
url = "https://playground.learnqa.ru/api/homework_header"
key = "x-secret-homework-header"
value = "Some secret value"


def test_something_headers():
    response = requests.get(url)
    print()
    print(dict(response.headers))

    assert response.headers, "There is no headers in the response"
    try:
        assert key in response.headers, f"There is no key {key} in the headers"
        assert value in dict(response.headers).values(), f"There is no value {value} on key {key} in the headers"
    except json.JSONDecodeError:
        assert False, f"Response headers is not in JSON format. Response text is '{response.headers}'"
