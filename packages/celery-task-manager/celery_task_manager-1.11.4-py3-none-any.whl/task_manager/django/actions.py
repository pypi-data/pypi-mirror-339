from datetime import timedelta
from functools import lru_cache
from typing import Any, Callable

from asgiref.sync import sync_to_async
from django.db.models import QuerySet
from django.utils import timezone

from task_manager.core.actions import get_fn_desc, parse_payload
from task_manager.django.models import ScheduledTask

DELTA_UNITS = {
    "s": lambda n: timedelta(seconds=n),
    "m": lambda n: timedelta(minutes=n),
    "h": lambda n: timedelta(hours=n),
    "d": lambda n: timedelta(days=n),
    "w": lambda n: timedelta(weeks=n),
}


class ScheduledTaskManager:
    def __init__(self, task: Callable, eta: str) -> None:
        self._task = task

        if callable(task) is False:
            raise ValueError("Task must be callable.")

        if hasattr(task, "delay") is False:
            raise ValueError("Task must be a Celery task.")

        self._set_eta(eta)

        self._module_name, self._function_name = get_fn_desc(task)

    def _set_eta(self, eta: str) -> None:
        self._eta = eta
        self._eta_number = eta[:-1]
        self._eta_unit = eta[-1]

        if self._eta_number.isnumeric() is False:
            raise ValueError("ETA value must be a number.")

        self._eta_number = int(self._eta_number)

        self._handler = DELTA_UNITS.get(self._eta_unit, None)
        if self._handler is None:
            raise ValueError(f"ETA unit must be one of {', '.join(DELTA_UNITS.keys())}.")

    def __call__(self, *args: Any, **kwargs: Any) -> None:
        return self.call(*args, **kwargs)

    def _get_delta(self) -> timedelta:
        return self._handler(self._eta_number)

    def call(self, *args: Any, **kwargs: Any) -> None:
        delta = self._get_delta()

        now = timezone.now()
        arguments = parse_payload(
            {
                "args": args,
                "kwargs": kwargs,
            }
        )

        ScheduledTask.objects.create(
            task_module=self._module_name,
            task_name=self._function_name,
            arguments=arguments,
            duration=delta,
            eta=now + delta,
        )

    @sync_to_async
    def acall(self, *args: Any, **kwargs: Any) -> None:
        return self.call(*args, **kwargs)

    def filter(self, *args: Any, **kwargs: Any) -> QuerySet[ScheduledTask]:
        now = timezone.now()
        arguments = parse_payload(
            {
                "args": args,
                "kwargs": kwargs,
            }
        )

        return ScheduledTask.objects.filter(
            task_module=self._module_name,
            task_name=self._function_name,
            arguments=arguments,
            eta__gte=now,
        )

    @sync_to_async
    def afilter(self, *args: Any, **kwargs: Any) -> QuerySet[ScheduledTask]:
        return self.filter(*args, **kwargs)

    def exists(self, *args: Any, **kwargs: Any) -> bool:
        return self.filter(*args, **kwargs).exists()

    @sync_to_async
    def aexists(self, *args: Any, **kwargs: Any) -> bool:
        return self.exists(*args, **kwargs)

    def copy(self) -> "ScheduledTaskManager":
        return ScheduledTaskManager(self._task, self._eta)

    def eta(self, eta, overwrite=False) -> "ScheduledTaskManager":
        if overwrite:
            self._set_eta(eta)
            schedule_task.cache_clear()
            return self

        return ScheduledTaskManager(self._task, eta)


@lru_cache
def schedule_task(task: Callable, eta: str) -> ScheduledTaskManager:
    """
    Schedule a task, it returns a scheduled task manager.

    Get a instance of the schedule manager.
    ```py
    schedule_manager = schedule_task(my_task, '1d')
    ```

    You should schedule the execution using:

    1. A direct call.
    ```py
    schedule_manager(1, 2, 3, name='my_task')
    ```

    2. Using the `call` function.
    ```py
    schedule_manager.call(1, 2, 3, name='my_task')
    ```

    3. Using the `acall` function.
    ```py
    await schedule_manager.acall(1, 2, 3, name='my_task')
    ```
    """

    return ScheduledTaskManager(task, eta)
