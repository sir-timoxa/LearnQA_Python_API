import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests


class TestUserEdit(BaseCase):
    def test_edit_just_created_user(self):
        # Register
        register_data = self.prepare_registration_data()
        response_first = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response_first, 200)
        Assertions.assert_json_has_key(response_first, "id")

        email = register_data['email']
        first_name = register_data['firstName']
        password = register_data['password']
        user_id = self.get_json_value(response_first, 'id')

        # login
        login_data = {
            "email": email,
            "password": password
        }

        response_second = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response_second, "auth_sid")
        token = self.get_header(response_second, "x-csrf-token")

        # Edit

        new_name = "Changed Name"

        response_third = MyRequests.put(f"/user/{user_id}",
                                      headers={"x-csrf-token": token},
                                      cookies={"auth_sid": auth_sid},
                                      data={"firstName": new_name}

                                      )

        Assertions.assert_code_status(response_third, 200)

        # Get

        response_fourth = MyRequests.get(f"/user/{user_id}",
                                       headers={"x-csrf-token": token},
                                       cookies={"auth_sid": auth_sid},
                                       )

        Assertions.assert_json_value_by_name(response_fourth,
                                             "firstName",
                                             new_name,
                                             "Wrong name of user after edit"
                                             )
