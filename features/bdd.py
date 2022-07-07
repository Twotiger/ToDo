import sys
from rich import print
from rich.console import Console

import json
import unittest
import requests
from urllib.parse import urljoin
# from aiohttp.test_utils import TestClient
from utils.password import gener_password
from todo.settings import SALT

BASE_URL = "http://127.0.0.1:8000"

test = unittest.TestCase()


class Client:
    def __init__(self, token=""):
        self.s = requests.Session()
        # 设置jwt token
        self.s.headers["Authorization"] = token
        self.s.headers["Content-Type"] = "application/json;charset=UTF-8"

    def post(self, url, json=None, **kwargs):
        url = urljoin(BASE_URL, url)
        return self.s.post(url, json=json, **kwargs)

    def get(self, url, params=None, **kwargs):
        url = urljoin(BASE_URL, url)
        return self.s.get(url, params=params, **kwargs)

    def put(self, url, data=None, **kwargs):
        url = urljoin(BASE_URL, url)
        return self.s.put(url, json=data, **kwargs)

    def delete(self, url, data, **kwargs):
        url = urljoin(BASE_URL, url)
        return self.s.delete(url, json=data, **kwargs)

    def patch(self, url, data, **kwargs):
        url = urljoin(BASE_URL, url)
        return self.s.patch(url, json=data, **kwargs)


def login(username: str) -> Client:
    password = "test"
    data = requests.post(
        BASE_URL + "/api/login", json={"username": username, "password": password}
    ).json()
    print("data=", data)
    client = Client(data["token"])
    return client


def create_user(username: str, is_super=False) -> None:
    from db.models import Account as AccountDB
    if is_super:
        AccountDB.objects.create_user(
            username=username,
            password="test",
            first_name=username,
            email="{}@test.com".format(username),
            is_superuser=True,
        )
    else:

        AccountDB.objects.create_user(
            username=username,
            password="test",
            first_name=username,
            email="{}@test.com".format(username),
        )


def red(value):
    return "\033[31;1m{}\033[0m".format(value)


def expected_(value):
    return "\033[32m{}\033[0m".format(value)


def actual_(value):
    return "\033[93m{}\033[0m".format(value)

console = Console()


class Expected:
    """ """

    def __init__(self, expected, rule: dict={}):
        self.expected = expected
        self.rule = rule # 对于在rule中的字段使用指定的函数来判断是否相等

    def validate(self, actual):
        if isinstance(actual, list):
            try:
                self.assert_list(self.expected, actual)
            except Exception as e:
                console.print(self.expected)
                console.print(actual)
                raise e

        elif isinstance(actual, dict):
            self.assert_dict(self.expected, actual, 0)

        else:
            raise ValueError("Not support value")

    def assert_list(self, expected: list, actual: list):
        index = 0
        test.assertEqual(len(expected), len(actual), msg="两个list的长度不一致")
        for expected_data, actual_data in zip(expected, actual):

            if isinstance(expected_data, dict):
                self.assert_dict(expected_data, actual_data, index)
            else:
                test.assertEqual(
                    expected_data, actual_data, red(
                        f"[期望]{expected_data}[实际]{actual_data}")
                )

            index += 1

    def assert_dict(self, expected: dict, actual: dict, index: int):
        for key, value in expected.items():
            if isinstance(value, dict):
                self.assert_dict(value, actual[key], index)
            elif isinstance(value, list):
                self.assert_list(value, actual[key])
            else:
                if key not in actual:
                    print("实际数据缺少关键字:", key)
                test.assertIn(key, actual)
                if key in self.rule:
                    self.rule[key](value, actual[key])
                else:
                    test.assertEqual(
                        value,
                        actual[key],
                        red(f"【期望[{index}]】:{value}【实际[{index}]】{actual[key]},key:{key}"),
                    )