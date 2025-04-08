# https://docs.celeryq.dev/en/stable/reference/celery.result.html#celery.result.AsyncResult.status

import importlib
import logging
from typing import Any

from celery import shared_task
from celery.result import AsyncResult

from task_manager.core.exceptions import RetryTask
from task_manager.core.settings import get_setting
from task_manager.django.decorators import task
from task_manager.django.dispatch import SIGNALS

from .models import TaskManager

logger = logging.getLogger(__name__)


PRIORITY = get_setting("TASK_MANAGER")


# do not use our own task decorator
@shared_task(bind=False, priority=PRIORITY)
def mark_task_as_cancelled(task_manager_id):
    logger.info(f"Running mark_task_as_cancelled for {task_manager_id}")

    x = TaskManager.objects.filter(id=task_manager_id).first()
    if x is None:
        logger.error(f"TaskManager {task_manager_id} not found")
        return

    if x.status not in ["PENDING", "PAUSED"]:
        logger.warning(f"TaskManager {task_manager_id} was already DONE")
        return

    pending_task = AsyncResult(x.task_id)
    if pending_task.status == "STARTED":
        logger.warning(f"TaskManager {task_manager_id} is being executed, skipping")
        return

    x.status = "CANCELLED"
    x.killed = pending_task.status == "SENT"

    pending_task.revoke(terminate=True)

    x.save()

    logger.info(f"TaskManager {task_manager_id} marked as CANCELLED")


# do not use our own task decorator
@shared_task(bind=False, priority=PRIORITY)
def mark_task_as_reversed(task_manager_id, *, force=False):
    logger.info(f"Running mark_task_as_reversed for {task_manager_id}")

    x = TaskManager.objects.filter(id=task_manager_id).first()
    if x is None:
        logger.error(f"TaskManager {task_manager_id} not found")
        return

    if x.reverse_module is None or x.reverse_name is None:
        logger.warning(f"TaskManager {task_manager_id} does not have a reverse function")
        return

    if not force and x.status != "DONE":
        logger.warning(
            f"TaskManager {task_manager_id} is '{x.status}', skipping, you could use force=True to reverse it"
        )
        return

    if force:
        pending_task = AsyncResult(x.task_id)
        pending_task.revoke(terminate=True)

    x.killed = False
    x.status = "REVERSED"
    x.save()

    module = importlib.import_module(x.reverse_module)
    function = getattr(module, x.reverse_name)
    function(*x.arguments["args"], **x.arguments["kwargs"])

    logger.info(f"TaskManager {task_manager_id} marked as REVERSED")


# do not use our own task decorator
@shared_task(bind=False, priority=PRIORITY)
def mark_task_as_paused(task_manager_id):
    logger.info(f"Running mark_task_as_paused for {task_manager_id}")

    x = TaskManager.objects.filter(id=task_manager_id).first()
    if x is None:
        logger.error(f"TaskManager {task_manager_id} not found")
        return

    if x.status != "PENDING":
        logger.warning(f"TaskManager {task_manager_id} is not running")
        return

    x.status = "PAUSED"

    x.save()

    logger.info(f"TaskManager {task_manager_id} marked as PAUSED")


# do not use our own task decorator
@shared_task(bind=False, priority=PRIORITY)
def mark_task_as_pending(task_manager_id, *, force=False):
    logger.info(f"Running mark_task_as_pending for {task_manager_id}")

    x = TaskManager.objects.filter(id=task_manager_id).first()
    if x is None:
        logger.error(f"TaskManager {task_manager_id} not found")
        return

    if x.status in ["DONE", "CANCELLED", "REVERSED"]:
        logger.warning(f"TaskManager {task_manager_id} is already DONE")
        return

    pending_task = AsyncResult(x.task_id)
    if force is False and pending_task.status == "SENT":
        logger.warning(f"TaskManager {task_manager_id} scheduled, skipping")
        return

    if pending_task.status == "STARTED":
        logger.warning(f"TaskManager {task_manager_id} is being executed, skipping")
        return

    x.status = "PENDING"
    x.killed = pending_task.status == "SENT"

    pending_task.revoke(terminate=True)

    x.save()

    module = importlib.import_module(x.task_module)
    function = getattr(module, x.task_name)
    function.delay(
        *x.arguments["args"],
        **{
            **x.arguments["kwargs"],
            "page": x.current_page + 1,
            "total_pages": x.total_pages,
            "task_manager_id": task_manager_id,
        },
    )

    logger.info(f"TaskManager {task_manager_id} marked as PENDING")


# do not use our own task decorator
@task(bind=False, priority=PRIORITY)
def execute_signal(
    signal_module: str, signal_name: str, sender_module: str, sender_name: str, pk: Any, extra: dict[str, Any], **_: Any
):
    logger.info(f"Running execute_signal for {signal_module} {signal_name}, {sender_module} {sender_name} {pk}")

    module = SIGNALS.get(signal_module, None)
    if module is None:
        raise Exception(f"Emisor {signal_module} wasn't loaded")

    signal = module.get(signal_name, None)
    if signal is None:
        raise Exception(f"Signal {signal_name} wasn't loaded")

    try:
        x = importlib.import_module(sender_module)

    except Exception:
        raise Exception(f"sender_module {sender_module} isn't valid")

    sender = getattr(x, sender_name, None)
    if sender is None:
        raise Exception(f"sender_name {sender_name} isn't valid")

    instance = sender.objects.filter(pk=pk).first()
    if instance is None:
        raise RetryTask(f"{sender.__name__} with pk={pk} wasn't found")

    signal.send(sender=sender, instance=instance, **extra)

    logger.info("Signal executed successfully")
