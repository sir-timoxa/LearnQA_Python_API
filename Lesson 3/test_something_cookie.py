import requests

url = "https://playground.learnqa.ru/api/homework_cookie"
key = "HomeWork"
value = "hw_value"


def test_something_cookies():
    response = requests.get(url)
    print()
    print(dict(response.cookies))
    assert response.cookies, "There is no cookies in the response"
    assert key in response.cookies, f"There is no key {key} in the cookies"
    assert value in dict(response.cookies).values(), f"There is no value {value} on key {key} in the cookies"
