import pytest
import requests
import allure

from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests


@allure.epic("Authorization cases")
class TestUserAuth(BaseCase):
    exclude_params = [
        ("no_cookie"),
        ("no_token")
    ]

    def setup_method(self):
        data = {
            "email": "vinkotov@example.com",
            "password": "1234"
        }

        response_first = MyRequests.post('/user/login', data=data)

        self.auth_sid = self.get_cookie(response_first, "auth_sid")
        self.token = self.get_header(response_first, "x-csrf-token")
        self.user_id_from_auth_method = self.get_json_value(response_first, "user_id")

    @allure.description("This test succsesfully authorized user by email and password")
    def test_auth_user(self):

        response_second = MyRequests.get("/user/auth", headers={"x-csrf-token": self.token},
                                         cookies={"auth_sid": self.auth_sid})
        Assertions.assert_json_value_by_name(
            response_second,
            "user_id",
            self.user_id_from_auth_method,
            "User id from auth method is not equal from check method"
        )

    @allure.description("This test check authorization states status w/o sending auth cookie or token")
    @pytest.mark.parametrize("condition", exclude_params)
    def test_negative_auth_check(self, condition):

        if condition == "no_cookie":
            response_second = MyRequests.get("/user/auth",headers={"x-csrf-token": self.token})
        else:
            response_second = MyRequests.get("/user/auth",cookies={"auth_sid": self.auth_sid})
        Assertions.assert_json_value_by_name(
            response_second,
            "user_id",
            0,
            f"User is authorised with condition {condition}"
        )
