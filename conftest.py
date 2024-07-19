import random

import pytest
import requests
from faker import Faker

from data import url, ingredients

fake = Faker()


@pytest.fixture(scope='function')
def payload():
    payload = {
        "email": fake.email(),
        "password": fake.password(),
        "name": fake.name()
    }
    return payload


@pytest.fixture(scope='function')
def payload_ing():
    ingredient_id = []
    r_ing = requests.get(url + ingredients)
    for i in range(len(r_ing.json()['data'])):
        ingredient_id.append(r_ing.json()['data'][i]['_id'])
    payload_ing = {"ingredients": [random.choice(ingredient_id), random.choice(ingredient_id)]}
    return payload_ing
