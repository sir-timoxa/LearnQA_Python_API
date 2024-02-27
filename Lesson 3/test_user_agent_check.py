import pytest
import requests
from lib.assertions import Assertions

url = "https://playground.learnqa.ru/ajax/api/user_agent_check"

payload_and_expected = [
    (
        'Mozilla/5.0 (Linux; U; Android 4.0.2; en-us; Galaxy Nexus Build/ICL53F) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',
        {'platform': 'Mobile', 'browser': 'No', 'device': 'Android'}),
    (
        'Mozilla/5.0 (iPad; CPU OS 13_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/91.0.4472.77 Mobile/15E148 Safari/604.1',
        {'platform': 'Mobile', 'browser': 'Chrome', 'device': 'iOS'}),
    ('Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
     {'platform': 'Googlebot', 'browser': 'Unknown', 'device': 'Unknown'}),
    (
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.100.0',
        {'platform': 'Web', 'browser': 'Chrome', 'device': 'No'}),
    (
        'Mozilla/5.0 (iPad; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
        {'platform': 'Mobile', 'browser': 'No', 'device': 'iPhone'}),

]


@pytest.mark.parametrize("data, expected", payload_and_expected)
def test_something_headers(data, expected):
    response = requests.get(url, headers={"User-Agent": data})

    platform = expected['platform']
    browser = expected['browser']
    device = expected['device']

    Assertions.assert_json_value_by_name(
        response,
        'platform',
        platform,
        f"Missmatch type of platform.\n Expected: {platform}.\n Result: {response.json()['platform']}\n Broken User Agent: {data}")

    Assertions.assert_json_value_by_name(
        response,
        'browser',
        browser,
        f"Missmatch type of browser.\n Expected: {browser}.\n Result: {response.json()['browser']}\n Broken User Agent: {data}")

    Assertions.assert_json_value_by_name(
        response,
        'device',
        device,
        f"Missmatch type of device.\n Expected: {device}.\n Result: {response.json()['device']}\n Broken User Agent: {data}")
