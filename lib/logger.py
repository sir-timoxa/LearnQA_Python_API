import datetime
import os

from requests import Response


class Logger:
    # work_path = (os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    filename = f"logs\log_" + str(datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")) + ".log"

    @classmethod
    def _write_log_to_file(cls, data: str):
        with open(cls.filename, 'a', encoding='utf-8') as logger_file:
            logger_file.write(data)

    @classmethod
    def add_request(cls, url: str, data: dict, headers: dict, cookies: dict, method: str):
        name_of_test = os.environ.get('PYTEST_CURRENT_TEST')

        data_to_add = "\n-----\n"
        data_to_add += f"Test: {name_of_test}\n"
        data_to_add += f"Time: {str(datetime.datetime.now())}\n"
        data_to_add += f"Request method: {method}\n"
        data_to_add += f"Request url: {url}\n"
        data_to_add += f"Request data: {data}\n"
        data_to_add += f"Request headers: {headers}\n"
        data_to_add += f"Request cookies: {cookies}\n"
        data_to_add += "\n"

        cls._write_log_to_file(data_to_add)

    @classmethod
    def add_response(cls, response: Response):
        cookies_as_dict = dict(response.cookies)
        headers_as_dict = dict(response.headers)

        data_to_add = f"Response code: {response.status_code}\n"
        data_to_add += f"Response text: {response.text}\n"
        data_to_add += f"Response header: {headers_as_dict}\n"
        data_to_add += f"Response cookie: {cookies_as_dict}\n"
        data_to_add += "\n-----\n"

        cls._write_log_to_file(data_to_add)
