import requests

url = "https://playground.learnqa.ru/ajax/api/compare_query_type"
methods = ["GET", "PUT", "POST", "DELETE"]

response_without_method = requests.post(url=url)
print(f"Answer without method: {response_without_method.text}")
print(f"Response without method: {response_without_method}",end="\n\n")

not_supported_response = requests.patch(url=url)
print(f"Answer not supported response: {not_supported_response.text}")
print(f"Not supported response: {not_supported_response}",end="\n\n")

response_with_right_method = requests.get(url=url, params={"method": methods[0]})
print(f"Answer with right method: {response_with_right_method.text}")
print(f"Response with right method: {response_with_right_method}",end="\n\n")

for method in methods:
    print(method)
    for param in methods:
        if method != "GET":
            print(
                f"For {method} request with method {param} answer is  {requests.request(method, url=url, data={'method': param}).text}")
            print(
                f"For {method} request with method {param} response is  {requests.request(method, url=url, data={'method': param})}")
        else:
            print(
                f"For {method} request with method {param} answer is  {requests.request(method, url=url, params={'method': param}).text}")
            print(
                f"For {method} request with method {param} response is  {requests.request(method, url=url, params={'method': param})}")
