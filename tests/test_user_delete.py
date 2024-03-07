import allure

from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions


class TestUserDelete(BaseCase):
    def test_delete_stable_user(self):
        # login
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        response_first = MyRequests.post("/user/login", data=data)

        auth_sid = self.get_cookie(response_first, "auth_sid")
        token = self.get_header(response_first, "x-csrf-token")

        # deleted
        response_second = MyRequests.delete(f"/user/2",
                                            headers={"x-csrf-token": token},
                                            cookies={"auth_sid": auth_sid}
                                            )

        Assertions.assert_code_status(response_second, 400)
        Assertions.assert_content(response_second, "Please, do not delete test users with ID 1, 2, 3, 4 or 5.")

    @allure.title("Удаление созданного юзера")
    @allure.description(
        "Тест создает юзера, логиниться используя его данные, удаляет его, и проверяет, что пользователь действительно удален")
    @allure.tag("Regression","Smoke","DeleteData")
    def test_delete_authorized_user(self):
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

        # deleted

        response_third = MyRequests.delete(f"/user/{user_id}",
                                           headers={"x-csrf-token": token},
                                           cookies={"auth_sid": auth_sid}
                                           )

        Assertions.assert_code_status(response_third, 200)

        # Get

        response_fourth = MyRequests.get(f"/user/{user_id}")
        Assertions.assert_content(response_fourth, "User not found")

    def test_delete_another_user(self):
        # Register
        register_data = self.prepare_registration_data()
        response_first = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response_first, 200)
        Assertions.assert_json_has_key(response_first, "id")

        # login
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        response_second = MyRequests.post("/user/login", data=data)

        auth_sid = self.get_cookie(response_second, "auth_sid")
        token = self.get_header(response_second, "x-csrf-token")

        # deleted
        response_third = MyRequests.delete(f"/user/2",
                                           headers={"x-csrf-token": token},
                                           cookies={"auth_sid": auth_sid}
                                           )

        Assertions.assert_code_status(response_third, 400)
        Assertions.assert_content(response_third, "Please, do not delete test users with ID 1, 2, 3, 4 or 5.")
