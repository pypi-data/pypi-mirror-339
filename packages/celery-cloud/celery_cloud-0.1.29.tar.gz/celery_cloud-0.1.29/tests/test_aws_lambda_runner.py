import pytest
from unittest.mock import patch, MagicMock
from celery_cloud.runners.aws_lambda import (
    TaskRoute,
    TaskExecutionException,
    EventDecodeException,
    MessageDecodeException,
    TaskDecodeException,
)
from celery_cloud.entities import SQSEvent, SQSMessage, Task
from celery_cloud.models.task_model import TaskModel
import json



# # ===================================
# # get_event
# # ===================================


# def test_get_event_valid():
#     result = get_event({"Records": []})
#     assert isinstance(result, SQSEvent)


# def test_get_event_invalid():
#     with pytest.raises(EventDecodeException):
#         get_event({"bad": "input"})



# # ===================================
# # get_task
# # ===================================


# def test_get_task_valid():
#     headers = {
#         "lang": "py",
#         "task": "test.fn",
#         "id": "abc",
#         "retries": 0,
#         "timelimit": [None, None],
#         "root_id": "abc",
#         "argsrepr": "[]",
#         "kwargsrepr": "{}",
#         "origin": "test",
#         "ignore_result": False,
#         "replaced_task_nesting": 0,
#         "stamps": {},
#     }
#     props = {
#         "correlation_id": "abc",
#         "reply_to": "r",
#         "delivery_mode": 2,
#         "delivery_info": {"exchange": "default", "routing_key": "task_queue"},
#         "priority": 0,
#         "body_encoding": "base64",
#         "delivery_tag": "xyz",
#     }
#     msg = SQSMessage(
#         body="{}",
#         content_encoding="utf-8",
#         content_type="application/json",
#         headers=headers,
#         properties=props,
#     )
#     task = get_task(msg)
#     assert task.task == "test.fn"


# def test_get_task_invalid_argsrepr():
#     headers = {
#         "lang": "py",
#         "task": "test.fn",
#         "id": "abc",
#         "retries": 0,
#         "timelimit": [None, None],
#         "root_id": "abc",
#         "argsrepr": "[INVALID",  # eval fallará aquí
#         "kwargsrepr": "{}",
#         "origin": "test",
#         "ignore_result": False,
#         "replaced_task_nesting": 0,
#         "stamps": {},
#     }
#     props = {
#         "correlation_id": "abc",
#         "reply_to": "r",
#         "delivery_mode": 2,
#         "delivery_info": {"exchange": "default", "routing_key": "task_queue"},
#         "priority": 0,
#         "body_encoding": "base64",
#         "delivery_tag": "xyz",
#     }
#     msg = SQSMessage(
#         body="{}",
#         content_encoding="utf-8",
#         content_type="application/json",
#         headers=headers,
#         properties=props,
#     )

#     with pytest.raises(TaskDecodeException) as exc:
#         get_task(msg)

#     assert "Exception getting task" in str(exc.value.message)
