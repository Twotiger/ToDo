import os
import django

from django.test.runner import DiscoverRunner



BEHAVE_DEBUG_ON_ERROR = False
os.environ["DJANGO_SETTINGS_MODULE"] = "todo.settings"
django.setup()


# def create_user(name: str):
    # from db.models import Account
    # Account(username=name, password="123456", email=name + "@gmail.com").save()
 

def clean():
    # from django.contrib.auth.models import User
    from db.models import TaskList, Task, Account
    # Account.objects.all().delete()
    TaskList.objects.all().delete()
    Task.objects.all().delete()
    Account.objects.all().update(my_day_count=0, important_count=0, task_count=0)


def before_all(context):
    context.config.logging_format = "%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s"
    context.config.logging_datefmt = "%Y-%m-%d %H:%M:%S"
    # context.test_runner = DiscoverRunner()
    # context.test_runner.setup_test_environment()
    import bdd
    # clean()

    context.bdd = bdd
    context.config.logging_format = "%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s"
    context.config.logging_datefmt = "%Y-%m-%d %H:%M:%S"

    # bdd.create_user("Bob")
    # bdd.create_user("Jim")
    # bdd.create_user("Tom")


# def after_all(context):
#     if hasattr(context, "test_db_config"):
#         context.test_runner.teardown_databases(context.test_db_config)
#         context.test_runner.teardown_test_environment()


def before_scenario(context, scenario):
    clean()


def after_scenario(context, scenario):
    ...
