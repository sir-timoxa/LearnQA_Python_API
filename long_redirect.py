import requests

response = requests.post('https://playground.learnqa.ru/api/long_redirect', allow_redirects=True)

last_response = response

print(len(response.history))
print(last_response.url)
