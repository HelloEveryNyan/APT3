from typing import Any
import pytest
import yaml
import requests

with open("config.yaml") as f:
    data = yaml.safe_load(f)

@pytest.fixture()
def login():
    res = requests.post(data["address"] + "gateway/login", data={"username": data["username"], "password": data["password"]})
    return res.json()["token"]

@pytest.fixture()
def testtext1():
    return "Новость дня"

@pytest.fixture()
def post_data():
    return {
        "title": "Заголовок поста",
        "description": "Описание поста",
        "content": "Содержание поста"
    }

@pytest.fixture()
def created_post(login: Any, post_data: dict[str, str]):
    header = {"X-Auth-Token": login}
    res = requests.post(data["address"] + "api/posts", headers=header, data=post_data)
    assert res.status_code == 200
    return post_data
