from behave import *
from behave.api.async_step import async_run_until_complete
import logging

import unittest

test = unittest.TestCase()

@given("'{user}'登录网站")
def step_impl(context, user):
    client = context.bdd.login(user)
    logging.info("client=%s", client)
    context.client = client


@then('得到错误提示"{err_msg}"')
def step_impl(context, err_msg):
    response_data = context.response.json()
    test.assertNotEqual(context.response.status_code, 200)
    test.assertEqual(response_data["errMsg"], err_msg)


@then("得到成功提示")
def step_impl(context):
    response_data = context.response
    if response_data.status_code >= 400:
        print("response_data=", response_data.json())
    test.assertLess(response_data.status_code, 400)
