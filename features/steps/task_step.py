import json
import unittest
from datetime import datetime, timedelta
from behave import *


test = unittest.TestCase()


def getDate(value: str) -> str:
    today = datetime.today()
    if value == "今天":
        return today.strftime("%Y-%m-%d %H:%M:%S")
    if value == "明天":
        today = today + timedelta(days=1)
        return today.strftime("%Y-%m-%d %H:%M:%S")

    return value


def getDay(value: str) -> str:  # 0000-00-00
    today = datetime.today()
    if value == "今天":
        return today.strftime("%Y-%m-%d")
    if value == "明天":
        today = today + timedelta(days=1)
        return today.strftime("%Y-%m-%d")
    return value


def localTime(utc):
    UTC_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
    utcTime = datetime.strptime(utc, UTC_FORMAT)
    localtime = utcTime + timedelta(hours=8)
    return localtime.strftime("%Y-%m-%d")


@when("添加任务")
def step_impl(context):
    from db.models import TaskList
    data = json.loads(context.text)
    if 'deadline' in data:
        data['deadline'] = getDate(data['deadline'])
    else:
        data["deadline"] = ''

    if 'notice' in data:
        data['notice'] = getDate(data['notice'])
    else:
        data["notice"] = ''

    if 'repeat' not in data:
        data["repeat"] = ''

    if "task_list_name" in data:
        task_list = TaskList.objects.get(name=data["task_list_name"])
        data["task_list_id"] = task_list.id

    response = context.client.post("/api/task/task", data)
    context.response = response


def same_day(expected, actual):
    assert getDay(expected) == localTime(actual)


@then("查询每日任务")
def step_impl(context):
    expected_data = json.loads(context.text)
    params = {"is_my_day": True}
    actual_data = context.client.get("/api/task/tasks", params=params).json()
    expected = context.bdd.Expected(expected_data, {"deadline": same_day})
    expected.validate(actual_data)

@then('查询默认任务列表')
def step_impl(context):
    expected_data = json.loads(context.text)

    params = {"tasks": True}
    actual_data = context.client.get(
        "api/task/tasks", params=params).json()

    expected = context.bdd.Expected(expected_data, {"deadline": same_day})
    expected.validate(actual_data)


@when('完成任务"{task_name}"')
def step_impl(context, task_name):
    from db.models import Task
    task = Task.objects.get(name=task_name)
    response = context.client.patch(
        "/api/task/task", {'task_id': task.id, 'op': "complete"})
    context.response = response


@when('将任务"{task_name}"添加到我的一天')
def step_impl(context, task_name):
    from db.models import Task
    task = Task.objects.get(name=task_name)
    response = context.client.patch(
        "/api/task/task", {'task_id': task.id, 'op': "add_my_day"})
    context.response = response


@when('将任务"{task_name}"从我的一天删除')
def step_impl(context, task_name):
    from db.models import Task
    task = Task.objects.get(name=task_name)
    response = context.client.patch(
        "/api/task/task", {'task_id': task.id, 'op': "delete_my_day"})
    context.response = response


@when('将任务"{task_name}"添加到重要')
def setp_impl(context, task_name):
    from db.models import Task
    task = Task.objects.get(name=task_name)
    response = context.client.patch(
        "/api/task/task", {'task_id': task.id, 'op': "add_important"})
    context.response = response


@when('将任务"{task_name}"从重要删除')
def setp_impl(context, task_name):
    from db.models import Task
    task = Task.objects.get(name=task_name)
    response = context.client.patch(
        "/api/task/task", {'task_id': task.id, 'op': "delete_important"})
    context.response = response

@when('删除任务"{task_name}"')
def setp_impl(context, task_name):
    from db.models import Task
    task = Task.objects.get(name=task_name)
    response = context.client.delete(
        "/api/task/task", {'task_id': task.id})
    context.response = response

@when('修改"{task_name}"的备注')
def setp_impl(context, task_name):
    from db.models import Task
    data = json.loads(context.text)

    task = Task.objects.get(name=task_name)
    response = context.client.patch(
        "/api/task/task", {'task_id': task.id, 'op': "update_remark", 'remark': data['remark']})
    context.response = response


@then('查询任务"{task_name}"')
def step_impl(context, task_name):
    from db.models import Task

    task = Task.objects.get(name=task_name)
    expected_data = json.loads(context.text)

    params = {"task_id": task.id}
    actual_data = context.client.get(
        "/api/task/task", params=params).json()["data"]

    expected = context.bdd.Expected(expected_data)
    expected.validate(actual_data)


@then('查询每日建议')
def setp_impl(context):
    expected_data = json.loads(context.text)
    actual_data = context.client.get(
        "/api/task/tasks", params={"suggest": True}
    ).json()['data']
    expected = context.bdd.Expected(expected_data)
    expected.validate(actual_data)