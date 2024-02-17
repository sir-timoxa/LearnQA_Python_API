import requests

url = "https://playground.learnqa.ru/ajax/api/compare_query_type"
methods = ["GET", "PUT", "POST", "DELETE"]

response_without_method = requests.post(url=url)
print(f"Response without method: {response_without_method.text}")

not_supported_response = requests.head(url=url)
print(f"Not supported response: {not_supported_response}")

response_with_right_method = requests.get(url=url, params={"method": methods[1]})
print(f"Response with right method: {response_with_right_method}")


for method in methods:
    print(method)
    for param in methods:
        if method != "GET":
            print(f"For {method} request with method {param} response is  {requests.request(method, url=url, data={'method': param})}")
        else:
            print(
                f"For {method} request with method {param} response is  {requests.request(method, url=url, params={'method': param})}")
