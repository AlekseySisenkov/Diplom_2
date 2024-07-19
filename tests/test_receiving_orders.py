import allure
import requests
from faker import Faker

from data import url, register, login, orders, user

fake = Faker()


class TestReceivingOrders:
    @allure.title('Получение заказов конкретного пользователя с авторизацией')
    def test_with_authorization(self, payload):
        r_creat = requests.post(url + register, data=payload)
        requests.post(url + login, data=payload, timeout=10)
        token = r_creat.json()['accessToken']
        r_orders = requests.get(url + orders, headers={'Authorization': token})
        requests.delete(url + user, headers={'Authorization': token})
        assert r_orders.status_code == 200 and r_orders.json()['success'] == True

    @allure.title('Получение заказов конкретного пользователя без авторизации')
    def test_without_authorization(self):
        r_orders = requests.get(url + orders)
        assert r_orders.status_code == 401 and r_orders.json()['message'] == "You should be authorised"
