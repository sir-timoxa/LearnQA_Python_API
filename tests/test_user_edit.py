import string
import random

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

    def test_edit_user_not_auth(self):
        # Register
        register_data = self.prepare_registration_data()
        response_first = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response_first, 200)
        Assertions.assert_json_has_key(response_first, "id")

        email = register_data['email']
        first_name = register_data['firstName']
        password = register_data['password']
        user_id = self.get_json_value(response_first, 'id')

        # Edit

        new_name = "Changed Name"

        response_second = MyRequests.put(f"/user/{user_id}",
                                         data={"firstName": new_name})

        Assertions.assert_code_status(response_second, 400)
        Assertions.asser_content(response_second, "Auth token not supplied")

    def test_edit_user_with_auth_other_user(self):
        # Register
        register_data = self.prepare_registration_data()
        response_first = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response_first, 200)
        Assertions.assert_json_has_key(response_first, "id")

        user_id_register = self.get_json_value(response_first, 'id')

        # login other user
        data = {
            "email": "vinkotov@example.com",
            "password": "1234"
        }

        response_second = MyRequests.post("/user/login", data=data)

        auth_sid = self.get_cookie(response_second, "auth_sid")
        token = self.get_header(response_second, "x-csrf-token")

        # Edit register user

        new_name = "Changed Name"

        response_third = MyRequests.put(f"/user/{user_id_register}",
                                        headers={"x-csrf-token": token},
                                        cookies={"auth_sid": auth_sid},
                                        data={"firstName": new_name}
                                        )

        Assertions.assert_code_status(response_third, 400)
        Assertions.asser_content(response_third, "Please, do not edit test users with ID 1, 2, 3, 4 or 5.")

    def test_edit_users_email_without_at(self):
        # Register
        register_data = self.prepare_registration_data()
        response_first = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response_first, 200)
        Assertions.assert_json_has_key(response_first, "id")

        email = register_data['email']
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

        new_email = "example_without_at"

        response_third = MyRequests.put(f"/user/{user_id}",
                                        headers={"x-csrf-token": token},
                                        cookies={"auth_sid": auth_sid},
                                        data={"email": new_email}
                                        )

        Assertions.assert_code_status(response_third, 400)
        Assertions.asser_content(response_third,"Invalid email format")

    def test_edit_user_first_name_very_short(self):
        # Register
        register_data = self.prepare_registration_data()
        response_first = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response_first, 200)
        Assertions.assert_json_has_key(response_first, "id")

        email = register_data['email']
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

        new_name = random.choice(string.ascii_letters)

        response_third = MyRequests.put(f"/user/{user_id}",
                                        headers={"x-csrf-token": token},
                                        cookies={"auth_sid": auth_sid},
                                        data={"firstName": new_name}
                                        )

        Assertions.assert_code_status(response_third, 400)
        Assertions.assert_json_value_by_name(response_third,
                                             "error",
                                             "Too short value for field firstName",
                                             "firstName became very short"
                                             )
