import json
import unittest

from behave import *
import logging

test = unittest.TestCase()


@when("添加任务列表")
def step_impl(context):
    from db.models import TaskList
    data = json.loads(context.text)
    data["task_type"] = "list"

    # if "parent" in data:
    #     # 查询
    #     model = TaskList.objects.get(name=data["parent"])
    #     data["parent_id"] = model.id

    response = context.client.post("/api/task_list/task_list", data)
    context.response = response


@when("添加任务组")
def step_impl(context):
    data = json.loads(context.text)
    data["task_type"] = "group"
    response = context.client.post("/api/task_list/task_list", data)
    context.response = response


@then("查询任务列表") # 弃用,使用 "查询任务列表详情"
def step_impl(context):
    expected_data = json.loads(context.text)
    actual_data = context.client.get("/api/task_list/task_lists").json()[
        "data"
    ]
    expected = context.bdd.Expected(expected_data)
    expected.validate(actual_data)


@then("查询任务列表详情")
def step_impl(context):
    expected_data = json.loads(context.text)
    actual_data = context.client.get("/api/task_list/task_lists").json()
    expected = context.bdd.Expected(expected_data)
    expected.validate(actual_data)

@when('移动任务列表"{from_task_name}"到"{to_task_name}"的"{position}"')
def step_impl(context, from_task_name, to_task_name, position):
    from db.models import TaskList
    position_dict = {
        "上面": "up",
        "下面": "down",
        "里面": "in"
    }
    position = position_dict[position]

    from_task = TaskList.objects.get(name=from_task_name)
    to_task = TaskList.objects.get(name=to_task_name)

    response = context.client.patch(
        "/api/task_list/task_lists", {"from_id": from_task.id, "to_id": to_task.id, "position": position})
    context.response = response


@when("随机测试任务列表")
def step_impl(context):
    from db.models import TaskList
    from random import choice
    count = TaskList.objects.count()
    mem = {}
    for task_list in TaskList.objects.all():
        mem[task_list.id] = task_list

    count = 100
    while count > 0:
        from_task = mem[choice(list(mem.keys()))]
        to_task = mem[choice(list(mem.keys()))]
        position = choice(["up", "down", "in"])
        logging.info("%s, %s, %s", from_task.name, to_task.name, position)
        response = context.client.patch(
            "/api/task_list/task_lists", {"from_id": from_task.id, "to_id": to_task.id, "position": position})
        logging.info("%s", response.json())
        count -= 1
        check()


def check():
    from db.models import TaskList

    models = TaskList.objects.filter().order_by("parent_id", "index")
    data = []
    mem = {}
    first_set = set()
    second_dict = {}
    for model in models:
        logging.info("name:%s index:%s parent_id:%s id:%s",
                     model.name, model.index, model.parent_id, model.id)
        if model.parent_id == 0:

            if model.index in first_set:
                raise ValueError
            first_set.add(model.index)
        else:

            second_dict.setdefault(model.parent_id, [])
            if model.index in second_dict[model.parent_id]:
                raise ValueError
            second_dict[model.parent_id].append(model.index)
