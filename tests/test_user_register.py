import string
import random

import pytest
from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests


class TestUserRegister(BaseCase):

    def test_create_user_successfully(self):
        data = self.prepare_registration_data()

        response = MyRequests.post("/user", data=data)
        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

    def test_create_user_with_existing_email(self):
        email = "vinkotov@example.com"
        data = self.prepare_registration_data(email)

        response = MyRequests.post("/user", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode(
            'utf-8') == f"Users with email '{email}' already exists", f"Unexpected response content {response.content.decode('utf-8')}"

    def test_create_user_without_at(self):
        email = "emailwithoutatexample.com"
        data = self.prepare_registration_data(email)

        response = MyRequests.post("/user", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode(
            'utf-8') == f"Invalid email format", f"Unexpected response content {response.content.decode('utf-8')}"

    parameters = [
        ("password"),
        ("username"),
        ("firstName"),
        ("lastName"),
        ("email")
    ]

    @pytest.mark.parametrize('parameter', parameters)
    def test_create_user_without_required_parameter(self, parameter):
        data = self.prepare_registration_data()
        data.pop(parameter)
        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The following required params are missed: {parameter}", \
            f"Unexpected response content {response.content}"

    def test_create_user_with_very_short_name(self):
        email = "vinkotov@example.com"
        name = random.choice(string.ascii_letters)
        my_data = {'password': '123', 'username': name, 'firstName': 'learnqa', 'lastName': 'learnqa', 'email': email}
        response = MyRequests.post("/user/", data=my_data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode(
            'utf-8') == f"The value of 'username' field is too short", f"Unexpected response content {response.content.decode('utf-8')}"

    def test_create_user_with_very_long_name(self):
        email = "vinkotov@example.com"
        name = ''.join(random.choice(string.ascii_letters) for i in range(256))
        my_data = {'password': '123', 'username': name, 'firstName': 'learnqa', 'lastName': 'learnqa', 'email': email}
        response = MyRequests.post("/user/", data=my_data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode(
            'utf-8') == f"The value of 'username' field is too long", f"Unexpected response content {response.content.decode('utf-8')}"