import allure
import requests
from faker import Faker

from data import url, register, user

fake = Faker()


class TestCreatUser:
    @allure.title('Cоздание уникального пользователя')
    def test_creat_unique_user(self, payload):
        r_creat = requests.post(url+register, data=payload)
        token = r_creat.json()['accessToken']
        r_del = requests.delete(url + user, headers={'Authorization': token})
        assert r_creat.status_code == 200 and r_creat.json()['success'] == True

    @allure.title('Cоздание уже зарегистрированного пользователя')
    def test_creat_registered_user(self, payload):
        r = requests.post(url+register, data=payload)
        r_double = requests.post(url+register, data=payload)
        token = r.json()['accessToken']
        requests.delete(url + user, headers={'Authorization': token})
        assert r_double.status_code == 403 and r_double.json()['message'] == "User already exists"

    @allure.title('Cоздание пользователя с незаполненным полем')
    def test_creat_user_without_field(self):
        payload = {
            "email": "",
            "password": fake.password(),
            "name": fake.name()
        }
        r = requests.post(url+register, data=payload)
        assert r.status_code == 403 and r.json()['message'] == "Email, password and name are required fields"

