import re
from unittest.mock import MagicMock, call

import pytest
from django.contrib.auth.models import Group
from faker import Faker

from task_manager.core.exceptions import AbortTask
from task_manager.django import decorators

# enable this file to use the database
pytestmark = pytest.mark.usefixtures("db")
fake = Faker()


class CustomException(Exception):

    def __eq__(self, other):
        return isinstance(other, CustomException) and str(self) == str(other)


def get_inner_fn():
    m = MagicMock()

    def inner_fn(*args, **kwargs):
        key = next(iter(kwargs.keys()))

        # this is used for testing the rollback
        value = str(kwargs[key])
        Group.objects.create(name=value)

        if "MUST_BE_ABORTED" in kwargs and kwargs["MUST_BE_ABORTED"] is True:
            e = AbortTask("It was aborted")
            m(e)
            raise e

        if "MUST_RAISE_EXCEPTION" in kwargs and kwargs["MUST_RAISE_EXCEPTION"] is True:
            e = CustomException("Unexpected error")
            m(e)
            raise e

        if len(args) == 5:
            kwargs["WITH_SELF"] = True

        m(*args, **kwargs)

    return inner_fn, m


# it's to can reverse a task through the task manager
def reverse(*args, **kwargs):
    return args, kwargs


def fallback(*args, exception=None, **kwargs):
    kwargs["exception"] = f"{type(exception)}: {str(exception)}"

    Group.objects.create(name="fallback city")

    return 1, args, kwargs, 2


@pytest.fixture
def setup(database, get_json_obj, fake, monkeypatch, get_args, get_kwargs):

    def _arrange(*, task_manager, transaction=None, bind=False, with_fallback=False, with_reverse=False):
        inner_fn, m = get_inner_fn()
        c = MagicMock()
        name = fake.slug().replace("-", "_")

        inner_fn.__name__ = name
        inner_fn.__module__ = "breathecode.commons.tasks"

        reverse.__module__ = "breathecode.commons.tasks"

        params = {
            "bind": bind,
            "transaction": transaction,
        }

        if with_fallback:
            params["fallback"] = fallback

        if with_reverse:
            params["reverse"] = reverse

        task = decorators.task(**params)(inner_fn)
        monkeypatch.setattr(decorators.Task, "_get_fn", lambda self, task_module, task_name: task)

        setattr(c, name, MagicMock(side_effect=task))

        monkeypatch.setattr("task_manager.django.tasks", c)
        model = database.create(task_manager=task_manager)

        args = get_args(4)
        kwargs = get_kwargs(4)

        # return model, task, name, args, kwargs, lambda: getattr(c, name).call_args_list
        city_code = next(iter(kwargs.keys()))
        return model, task, name, args, kwargs, city_code, m

    yield _arrange


def db_item(data={}):
    return {
        "arguments": {
            "args": ["resource-reflect", 25, 38.21, 49.74],
            "kwargs": {
                "minute-agree-spring": "range-so-power-drop",
                "public-western": 15.88,
                "something-along": 47,
                "street-book": 20.36,
                "task_manager_id": 1,
            },
        },
        "attempts": 1,
        "current_page": 1,
        "id": 1,
        "killed": False,
        "last_run": ...,
        "reverse_module": None,
        "reverse_name": None,
        "exception_module": None,
        "exception_name": None,
        "status": "DONE",
        "fixed": False,
        "priority": None,
        "status_message": None,
        "task_module": "breathecode.commons.tasks",
        "task_name": "",
        "total_pages": 1,
        **data,
    }


# When: 0 TaskManager's
# Then: it should create a new TaskManager and call the task
def test_no_task_manager(database, get_json_obj, setup, utc_now, monkeypatch):
    _, task, task_name, args, kwargs, city_code, result = setup(
        task_manager=0, bind=False, with_fallback=False, with_reverse=False, transaction=False
    )

    # assert res == (args, {**kwargs, 'task_manager_id': 1})
    monkeypatch.setattr("uuid.UUID.hex", lambda: "asdasdasd")
    res = task(*args, **kwargs)

    from celery import Task

    Task.delay

    assert res is None
    assert result.call_args_list == [call(*args, **{**kwargs, "task_manager_id": 1})]

    db = [
        x
        for x in database.list_of("task_manager.TaskManager")
        if re.search(r"^[a-zA-Z0-9-]+$", x["task_id"]) and x.pop("task_id")
    ]

    assert db == [
        db_item(
            {
                "arguments": {
                    "args": list(args),
                    "kwargs": {
                        **kwargs,
                        "task_manager_id": 1,
                    },
                },
                "status": "SCHEDULED",
                "last_run": utc_now,
                "started_at": None,
                "task_name": task_name,
                "current_page": 0,
                "total_pages": 1,
                "priority": 5,
            }
        ),
    ]

    # this is used for testing the rollback
    assert database.list_of("auth.Group") == [
        {
            "id": 1,
            "name": str(kwargs[city_code]),
        },
    ]


# When: 0 TaskManager's
# Then: it should create a new TaskManager and call the task
def test_scheduled_task_manager_is_being_exec(database, get_json_obj, setup, utc_now, fake):
    model, task, task_name, args, kwargs, city_code, result = setup(
        task_manager=1, bind=False, with_fallback=False, with_reverse=False, transaction=False
    )

    id = fake.uuid4()

    model.task_manager.status = "SCHEDULED"
    model.task_manager.arguments = {
        "args": list(args),
        "kwargs": {
            **kwargs,
            "task_manager_id": 1,
        },
    }

    model.task_manager.task_module = "breathecode.commons.tasks"
    model.task_manager.task_name = task_name
    model.task_manager.task_id = id
    model.task_manager.save()

    res = task(*args, **kwargs, task_manager_id=1)

    # assert res == (args, {**kwargs, 'task_manager_id': 1})

    assert res is None
    assert result.call_args_list == [call(*args, **{**kwargs, "task_manager_id": 1})]

    assert database.list_of("task_manager.TaskManager") == [
        db_item(
            {
                "arguments": {
                    "args": list(args),
                    "kwargs": {
                        **kwargs,
                        "task_manager_id": 1,
                    },
                },
                "status": "DONE",
                "last_run": utc_now,
                "started_at": utc_now,
                "task_name": task_name,
                "task_id": id,
                "current_page": 1,
                "total_pages": 1,
                "status_message": "",
            }
        ),
    ]

    # this is used for testing the rollback
    assert database.list_of("auth.Group") == [
        {
            "id": 1,
            "name": str(kwargs[city_code]),
        },
    ]


# Given: 0 TaskManager's
# When: it's aborted
# Then: it should create a new TaskManager and call the task,
#    -> and save it as aborted even if transaction=True
@pytest.mark.parametrize("transaction", [True, False, None])
def test_no_task_manager__it_was_aborted(database, get_json_obj, setup, utc_now, transaction, fake):
    model, task, task_name, args, kwargs, city_code, result = setup(
        task_manager=1, bind=False, with_fallback=False, with_reverse=False, transaction=transaction
    )

    id = fake.uuid4()
    kwargs["MUST_BE_ABORTED"] = True

    model.task_manager.status = "SCHEDULED"
    model.task_manager.arguments = {
        "args": list(args),
        "kwargs": {
            **kwargs,
            "task_manager_id": 1,
        },
    }

    model.task_manager.task_module = "breathecode.commons.tasks"
    model.task_manager.task_name = task_name
    model.task_manager.task_id = id
    model.task_manager.save()

    res = task(*args, **kwargs, task_manager_id=1)

    assert res is None
    assert result.call_args_list == [call(AbortTask("It was aborted"))]

    assert database.list_of("task_manager.TaskManager") == [
        db_item(
            {
                "arguments": {
                    "args": list(args),
                    "kwargs": {
                        **kwargs,
                        "task_manager_id": 1,
                    },
                },
                "status": "ABORTED",
                "last_run": utc_now,
                "started_at": utc_now,
                "task_name": task_name,
                "task_id": id,
                "current_page": 1,
                "total_pages": 1,
                "status_message": "It was aborted",
                "exception_module": "task_manager.core.exceptions",
                "exception_name": "AbortTask",
            }
        ),
    ]

    # this is used for testing the rollback
    assert database.list_of("auth.Group") == [
        {
            "id": 1,
            "name": str(kwargs[city_code]),
        },
    ]


# Given: 0 TaskManager's
# When: it had an exception, no fallback
# Then: it should create a new TaskManager and call the task,
#    -> and save it as error even if transaction=True
@pytest.mark.parametrize("with_fallback", [False, None])
@pytest.mark.parametrize("transaction", [False, None])
def test_no_task_manager__it_got_an_exception__no_transaction__no_fallback(
    database, get_json_obj, setup, utc_now, transaction, with_fallback, fake
):
    model, task, task_name, args, kwargs, city_code, result = setup(
        task_manager=1, bind=False, with_fallback=with_fallback, with_reverse=False, transaction=transaction
    )

    id = fake.uuid4()
    kwargs["MUST_RAISE_EXCEPTION"] = True

    model.task_manager.status = "SCHEDULED"
    model.task_manager.arguments = {
        "args": list(args),
        "kwargs": {
            **kwargs,
            "task_manager_id": 1,
        },
    }

    model.task_manager.task_module = "breathecode.commons.tasks"
    model.task_manager.task_name = task_name
    model.task_manager.task_id = id
    model.task_manager.save()

    task.delay(*args, **kwargs, task_manager_id=1)

    assert database.list_of("task_manager.TaskManager") == [
        db_item(
            {
                "arguments": {
                    "args": list(args),
                    "kwargs": {
                        **kwargs,
                        "task_manager_id": 1,
                    },
                },
                "status": "ERROR",
                "last_run": utc_now,
                "task_name": task_name,
                "started_at": utc_now,
                "task_id": id,
                "current_page": 1,
                "total_pages": 1,
                "status_message": "Unexpected error",
                "exception_module": "tests.django.decorators.test_task",
                "exception_name": "CustomException",
            }
        ),
    ]

    # this is used for testing the rollback
    assert database.list_of("auth.Group") == [
        {
            "id": 1,
            "name": str(kwargs[city_code]),
        },
    ]


# Given: 0 TaskManager's
# When: it had an exception, with fallback
# Then: it should create a new TaskManager and call the task,
#    -> save it as error even if transaction=True
#    -> and call the fallback
@pytest.mark.parametrize("transaction", [False, None])
def test_no_task_manager__it_got_an_exception__no_transaction__with_fallback(
    database, get_json_obj, setup, utc_now, transaction, fake
):
    model, task, task_name, args, kwargs, city_code, result = setup(
        task_manager=1, bind=False, with_fallback=True, with_reverse=False, transaction=transaction
    )

    id = fake.uuid4()
    kwargs["MUST_RAISE_EXCEPTION"] = True

    model.task_manager.status = "SCHEDULED"
    model.task_manager.arguments = {
        "args": list(args),
        "kwargs": {
            **kwargs,
            "task_manager_id": 1,
        },
    }

    model.task_manager.task_module = "breathecode.commons.tasks"
    model.task_manager.task_name = task_name
    model.task_manager.task_id = id
    model.task_manager.save()

    res = task(*args, **kwargs, task_manager_id=1)

    assert res == (
        1,
        args,
        {
            **kwargs,
            "task_manager_id": 1,
            "exception": "<class 'tests.django.decorators.test_task.CustomException'>: Unexpected error",
        },
        2,
    )
    assert result.call_args_list == [call(CustomException("Unexpected error"))]

    assert database.list_of("task_manager.TaskManager") == [
        db_item(
            {
                "arguments": {
                    "args": list(args),
                    "kwargs": {
                        **kwargs,
                        "task_manager_id": 1,
                    },
                },
                "status": "ERROR",
                "last_run": utc_now,
                "task_name": task_name,
                "started_at": utc_now,
                "task_id": id,
                "current_page": 1,
                "total_pages": 1,
                "status_message": "Unexpected error",
                "exception_module": "tests.django.decorators.test_task",
                "exception_name": "CustomException",
            }
        ),
    ]

    # this is used for testing the rollback
    assert database.list_of("auth.Group") == [
        {
            "id": 1,
            "name": str(kwargs[city_code]),
        },
        {
            "id": 2,
            "name": "fallback city",
        },
    ]


# Given: 0 TaskManager's
# When: it had an exception, with transaction and no fallback
# Then: it should create a new TaskManager and call the task,
#    -> it reverse the database (City)
def test_no_task_manager__it_got_an_exception__with_transaction__no_fallback(
    database, get_json_obj, setup, utc_now, fake
):
    model, task, task_name, args, kwargs, _, result = setup(
        task_manager=1, bind=False, with_fallback=False, with_reverse=False, transaction=True
    )

    id = fake.uuid4()
    kwargs["MUST_RAISE_EXCEPTION"] = True

    model.task_manager.status = "SCHEDULED"
    model.task_manager.arguments = {
        "args": list(args),
        "kwargs": {
            **kwargs,
            "task_manager_id": 1,
        },
    }

    model.task_manager.task_module = "breathecode.commons.tasks"
    model.task_manager.task_name = task_name
    model.task_manager.task_id = id
    model.task_manager.save()

    task.delay(*args, **kwargs, task_manager_id=1)

    assert database.list_of("task_manager.TaskManager") == [
        db_item(
            {
                "arguments": {
                    "args": list(args),
                    "kwargs": {
                        **kwargs,
                        "task_manager_id": 1,
                    },
                },
                "status": "ERROR",
                "last_run": utc_now,
                "started_at": utc_now,
                "task_name": task_name,
                "task_id": id,
                "current_page": 1,
                "total_pages": 1,
                "status_message": "Unexpected error",
                "exception_module": "tests.django.decorators.test_task",
                "exception_name": "CustomException",
            }
        ),
    ]

    # this is used for testing the rollback
    assert database.list_of("auth.Group") == []


# Given: 0 TaskManager's
# When: it had an exception, with transaction and fallback
# Then: it should create a new TaskManager and call the task,
#    -> it reverse the database (City) and save elements from the fallback (City)
def test_no_task_manager__it_got_an_exception__with_transaction__with_fallback(
    database, get_json_obj, setup, utc_now, fake
):

    #####################################

    model, task, task_name, args, kwargs, _, result = setup(
        task_manager=1, bind=False, with_fallback=True, with_reverse=False, transaction=True
    )

    id = fake.uuid4()
    kwargs["MUST_RAISE_EXCEPTION"] = True

    model.task_manager.status = "SCHEDULED"
    model.task_manager.arguments = {
        "args": list(args),
        "kwargs": {
            **kwargs,
            "task_manager_id": 1,
        },
    }

    model.task_manager.task_module = "breathecode.commons.tasks"
    model.task_manager.task_name = task_name
    model.task_manager.task_id = id
    model.task_manager.save()

    res = task(*args, **kwargs, task_manager_id=1)

    assert res == (
        1,
        args,
        {
            **kwargs,
            "task_manager_id": 1,
            "exception": "<class 'tests.django.decorators.test_task.CustomException'>: Unexpected error",
        },
        2,
    )

    assert result.call_args_list == [call(CustomException("Unexpected error"))]

    assert database.list_of("task_manager.TaskManager") == [
        db_item(
            {
                "arguments": {
                    "args": list(args),
                    "kwargs": {
                        **kwargs,
                        "task_manager_id": 1,
                    },
                },
                "status": "ERROR",
                "last_run": utc_now,
                "task_name": task_name,
                "task_id": id,
                "started_at": utc_now,
                "current_page": 1,
                "total_pages": 1,
                "status_message": "Unexpected error",
                "exception_module": "tests.django.decorators.test_task",
                "exception_name": "CustomException",
            }
        ),
    ]

    # this is used for testing the rollback
    assert database.list_of("auth.Group") == [
        {
            "id": 1,
            "name": "fallback city",
        },
    ]


# When: 2 TaskManager's
# Then: it should update the first TaskManager and call the task
def test_two_task_managers(database, get_json_obj, setup, utc_now):
    task_manager = {"total_pages": 2}
    model, task, _, args, kwargs, city_code, result = setup(
        task_manager=(2, task_manager), bind=False, with_fallback=False, with_reverse=False, transaction=False
    )

    res = task(*args, **kwargs, task_manager_id=1)

    assert res is None
    assert result.call_args_list == [call(*args, **{**kwargs, "task_manager_id": 1})]

    assert database.list_of("task_manager.TaskManager") == [
        {
            **get_json_obj(model.task_manager[0]),
            "status": "PENDING",
            "last_run": utc_now,
            "current_page": 1,
            "total_pages": 2,
            "status_message": "",
        },
        get_json_obj(model.task_manager[1]),
    ]

    # this is used for testing the rollback
    assert database.list_of("auth.Group") == [
        {
            "id": 1,
            "name": str(kwargs[city_code]),
        },
    ]


# When: 2 TaskManager's
# Then: it should update the first TaskManager and mark it as killed
@pytest.mark.parametrize("status", ["CANCELLED", "REVERSED", "PAUSED", "ABORTED", "DONE"])
def test_two_task_managers__it_must_be_killed(database, get_json_obj, setup, utc_now, status):
    task_manager = {
        "total_pages": 2,
        "status": status,
        "killed": False,
    }
    model, task, _, args, kwargs, _, result = setup(
        task_manager=(2, task_manager), bind=False, with_fallback=False, with_reverse=False, transaction=False
    )

    res = task(*args, **kwargs, task_manager_id=1)

    assert res is None
    assert result.call_args_list == []

    assert database.list_of("task_manager.TaskManager") == [
        {
            **get_json_obj(model.task_manager[0]),
            "status": status,
            "last_run": utc_now,
            "current_page": 0,
            "total_pages": 2,
            "killed": True,
        },
        get_json_obj(model.task_manager[1]),
    ]

    # this is used for testing the rollback
    assert database.list_of("auth.Group") == []
