import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests


class TestUserGet(BaseCase):
    def test_get_user_details_not_auth(self):
        response = MyRequests.get("/user/2")

        Assertions.assert_json_has_key(response, 'username')
        Assertions.assert_json_has_not_key(response, 'email')
        Assertions.assert_json_has_not_key(response, 'firstName')
        Assertions.assert_json_has_not_key(response, 'lastName')

    def test_get_user_details_auth_as_same_user(self):
        data = {
            "email": "vinkotov@example.com",
            "password": "1234"
        }

        response_first = MyRequests.post("/user/login", data=data)

        auth_sid = self.get_cookie(response_first, "auth_sid")
        token = self.get_header(response_first, "x-csrf-token")
        user_id_from_auth_method = self.get_json_value(response_first, "user_id")

        response_second = MyRequests.get(f"/user/{user_id_from_auth_method}",
                                       headers={"x-csrf-token": token},
                                       cookies={"auth_sid": auth_sid})
        expected_fields = ["username", "email", "firstName", "lastName"]
        Assertions.assert_json_has_keys(response_second, expected_fields)

    def test_get_user_detail_not_auth(self):
        response = MyRequests.get("/user/2")
        Assertions.assert_json_has_key(response, "username")
        Assertions.assert_json_has_not_keys(response, ["email", "firstName", "lastName"])