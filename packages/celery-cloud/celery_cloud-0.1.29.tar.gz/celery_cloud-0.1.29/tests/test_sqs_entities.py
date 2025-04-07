import base64
import json
import pytest

from celery_cloud.entities import Task
from celery_cloud.entities.sqs_entities import (
    DeliveryInfo,
    Properties,
    Headers,
    SQSMessage,
    SQSRecord,
    SQSAttributes,
    SQSEvent,
)
from celery_cloud.exceptions import TaskDecodeException, EventDecodeException


def create_valid_headers(**overrides):
    data = {
        "lang": "py",
        "task": "my.task",
        "id": "abc123",
        "shadow": None,
        "eta": None,
        "expires": None,
        "group": None,
        "group_index": None,
        "retries": 0,
        "timelimit": [None, None],
        "root_id": "abc123",
        "parent_id": None,
        "argsrepr": "[]",
        "kwargsrepr": "{}",
        "origin": "unittest",
        "ignore_result": False,
        "replaced_task_nesting": 0,
        "stamped_headers": None,
        "stamps": {},
    }
    return Headers(**{**data, **overrides})


def create_valid_properties():
    return Properties(
        correlation_id="corr-id",
        reply_to="reply-queue",
        delivery_mode=2,
        delivery_info=DeliveryInfo(exchange="default", routing_key="task_queue"),
        priority=0,
        body_encoding="base64",
        delivery_tag="tag-1",
    )


def test_decode_body():
    original = {"hello": "world"}
    body = base64.b64encode(json.dumps(original).encode()).decode()
    msg = SQSMessage(
        body=body,
        content_encoding="utf-8",
        content_type="application/json",
        headers=create_valid_headers(),
        properties=create_valid_properties(),
    )
    assert msg.decode_body() == original


def test_get_task_success():
    msg = SQSMessage(
        body=base64.b64encode(json.dumps({}).encode()).decode(),
        content_encoding="utf-8",
        content_type="application/json",
        headers=create_valid_headers(argsrepr="['arg1']", kwargsrepr="{'x': 1}"),
        properties=create_valid_properties(),
    )
    task = msg.get_task()
    assert isinstance(task, Task)
    assert task.task == "my.task"
    assert task.args == ["arg1"]
    assert task.kwargs == {"x": 1}


def test_get_task_invalid_args():
    msg = SQSMessage(
        body=base64.b64encode(json.dumps({}).encode()).decode(),
        content_encoding="utf-8",
        content_type="application/json",
        headers=create_valid_headers(argsrepr="INVALID(", kwargsrepr="{}"),
        properties=create_valid_properties(),
    )
    with pytest.raises(TaskDecodeException) as exc:
        msg.get_task()
    assert "Exception getting task" in str(exc.value)


def test_sqs_record_get_message():
    content = {"foo": "bar"}
    body = base64.b64encode(json.dumps(content).encode()).decode()
    record = SQSRecord(
        messageId="msg-1",
        receiptHandle="abc",
        body=body,
        attributes=SQSAttributes(
            ApproximateReceiveCount="1",
            SentTimestamp="1234567890",
            ApproximateFirstReceiveTimestamp="1234567891",
        ),
        eventSource="aws:sqs",
        eventSourceARN="arn:aws:sqs:eu-west-1:123456789012:my-queue",
    )
    assert record.get_message() == content


def test_sqs_event_from_lambda_success():
    raw_event = {
        "Records": [
            {
                "messageId": "msg-1",
                "receiptHandle": "abc",
                "body": base64.b64encode(json.dumps({"test": "ok"}).encode()).decode(),
                "attributes": {
                    "ApproximateReceiveCount": "1",
                    "SentTimestamp": "1234567890",
                    "ApproximateFirstReceiveTimestamp": "1234567891",
                },
                "eventSource": "aws:sqs",
                "eventSourceARN": "arn:aws:sqs:::my-queue",
            }
        ]
    }
    result = SQSEvent.from_lambda(raw_event)
    assert isinstance(result, SQSEvent)
    assert result.Records[0].messageId == "msg-1"


def test_sqs_event_from_lambda_invalid_structure():
    with pytest.raises(EventDecodeException) as exc:
        SQSEvent.from_lambda({"no_records": []})
    assert "Invalid SQS event format" in str(exc.value)
