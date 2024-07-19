import allure
import requests
from faker import Faker

from data import url, register, login, user, payload_mod

fake = Faker()


class TestModifiedUserData:
    @allure.title('Изменение данных пользователя с авторизацией')
    def test_with_authorization(self, payload):
        r_creat = requests.post(url + register, data=payload)
        requests.post(url + login, data=payload, timeout=10)
        token = r_creat.json()['accessToken']
        r_mod = requests.patch(url + user, data=payload_mod, headers={'Authorization': token}, timeout=10)
        requests.delete(url + user, headers={'Authorization': token})
        assert (r_mod.status_code == 200 and r_mod.json()['user']['name'] == "test_mod"
                and r_mod.json()['user']['email'] == "test_mod@test.org")

    @allure.title('Изменение данных пользователя без авторизации')
    def test_without_authorization(self):
        r_mod = requests.patch(url + user, data=payload_mod)
        assert r_mod.status_code == 401 and r_mod.json()['message'] == "You should be authorised"
