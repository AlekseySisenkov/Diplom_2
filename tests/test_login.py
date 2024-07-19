import allure
import requests

from data import url, register, login, user


class TestLogin:
    @allure.title('Авторизация под существующим пользователем')
    def test_login_existing_user(self, payload):
        r_creat = requests.post(url + register, data=payload)
        r_login = requests.post(url + login, data=payload, timeout=10)
        token = r_creat.json()['accessToken']
        requests.delete(url + user, headers={'Authorization': token})
        assert r_login.status_code == 200 and r_login.json()['success'] == True

    @allure.title('Авторизация с неверным логином и паролем')
    def test_incorrect_login(self, payload):
        r_login = requests.post(url + login, data=payload)
        assert r_login.status_code == 401 and r_login.json()['message'] == "email or password are incorrect"
