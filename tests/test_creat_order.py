import allure
import requests
from faker import Faker

from data import url, register, login, orders, user

fake = Faker()


class TestCreatOrder:
    @allure.title('Создание заказа с авторизацией')
    def test_with_authorization(self, payload, payload_ing):
        r_creat_user = requests.post(url + register, data=payload)
        r_login = requests.post(url + login, data=payload, timeout=10)
        token = r_creat_user.json()['accessToken']
        r_creat_order = requests.post(url + orders, data=payload_ing, headers={'Authorization': token})
        r_del = requests.delete(url + user, headers={'Authorization': token})
        assert r_creat_order.status_code == 200 and r_creat_order.json()['success'] == True

    @allure.title('Создание заказа без авторизации')
    def test_without_authorization(self, payload_ing):
        r_creat_order = requests.post(url + orders, data=payload_ing)
        assert r_creat_order.status_code == 200 and r_creat_order.json()['success'] == True

    @allure.title('Создание заказа с ингредиентами')
    def test_with_ingredients(self, payload_ing):
        r_creat_order = requests.post(url + orders, data=payload_ing)
        assert r_creat_order.status_code == 200 and r_creat_order.json()['success'] == True

    @allure.title('Создание заказа без ингредиентов')
    def test_without_ingredients(self):
        payload_ing = {"ingredients": []}
        r_creat_order = requests.post(url + orders, data=payload_ing)
        assert r_creat_order.status_code == 400 and r_creat_order.json()['message'] == "Ingredient ids must be provided"

    @allure.title('Создание заказа с неверным хешем ингредиентов')
    def test_without_ingredients(self):
        payload_ing = {"ingredients": ["test1", "test2"]}
        r_creat_order = requests.post(url + orders, data=payload_ing)
        assert r_creat_order.status_code == 500
