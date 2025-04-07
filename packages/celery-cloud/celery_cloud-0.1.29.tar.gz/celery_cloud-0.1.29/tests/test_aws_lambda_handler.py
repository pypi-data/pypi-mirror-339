from unittest.mock import patch, MagicMock
from celery_cloud.runners.aws_lambda import lambda_handler
from celery_cloud.entities import Task
import pytest


@pytest.fixture
def valid_sqs_event() -> dict:
    return {
        "Records": [
            {
                "messageId": "msg-2",
                "receiptHandle": "abc",
                "body": "{}",
                "attributes": {
                    "ApproximateReceiveCount": "1",
                    "SentTimestamp": "1234567890",
                    "SenderId": "test",
                    "ApproximateFirstReceiveTimestamp": "1234567891"
                },
                "messageAttributes": {},
                "md5OfBody": "xyz",
                "eventSource": "aws:sqs",
                "eventSourceARN": "arn:aws:sqs:eu-west-1:123456789012:my-queue",
                "awsRegion": "eu-west-1"
            }
        ]
    }


@patch("celery_cloud.runners.aws_lambda.SQSEvent.from_lambda")
@patch("celery_cloud.runners.aws_lambda.SQSMessage")
@patch("celery_cloud.runners.aws_lambda.TaskModel.insert_task")
@patch("celery_cloud.runners.aws_lambda.TaskModel.update_task")
@patch("celery_cloud.runners.aws_lambda.settings")
def test_lambda_handler_unsupported_task(
    mock_settings,
    mock_update_task,
    mock_insert_task,
    mock_sqs_message_class,
    mock_from_lambda,
    valid_sqs_event,
):
    # No tareas definidas en settings
    mock_settings.TASKS = {}

    task_id = "abc123"
    fake_task = Task(id=task_id, task="unknown.task", args=[], kwargs={})

    mock_record = MagicMock()
    mock_record.messageId = "msg-2"
    mock_record.get_message.return_value = {
        "body": "{}",
        "content-encoding": "utf-8",
        "content-type": "application/json",
        "headers": {
            "lang": "py",
            "task": "unknown.task",
            "id": task_id,
            "retries": 0,
            "timelimit": [None, None],
            "root_id": task_id,
            "argsrepr": "[]",
            "kwargsrepr": "{}",
            "origin": "unittest",
            "ignore_result": False,
            "replaced_task_nesting": 0,
            "stamps": {},
        },
        "properties": {
            "correlation_id": "abc",
            "reply_to": "r",
            "delivery_mode": 2,
            "delivery_info": {"exchange": "default", "routing_key": "task_queue"},
            "priority": 0,
            "body_encoding": "base64",
            "delivery_tag": "xyz",
        },
    }

    mock_sqs_message = MagicMock()
    mock_sqs_message.get_task.return_value = fake_task
    mock_sqs_message_class.return_value = mock_sqs_message

    mock_sqs_event = MagicMock()
    mock_sqs_event.Records = [mock_record]
    mock_from_lambda.return_value = mock_sqs_event

    result = lambda_handler(valid_sqs_event, context={})

    assert result["status"] == "completed"
    assert result["processed_messages"] == 0
    assert result["failed_messages"] == 1
    assert result["failed_tasks"][0]["task_id"] == task_id
    assert "not supported" in result["failed_tasks"][0]["error"]


@patch("celery_cloud.runners.aws_lambda.settings")
def test_lambda_handler_event_decode_error(mock_settings):
    from celery_cloud.exceptions import EventDecodeException

    broken_event = {"bad": "structure"}

    with patch("celery_cloud.runners.aws_lambda.SQSEvent.from_lambda") as mock_from_lambda:
        mock_from_lambda.side_effect = EventDecodeException("Bad format", "Extra details")

        result = lambda_handler(broken_event, context={})

        assert result["status"] == "error"
        assert result["message"] == "Bad format"
        assert result["details"] == "Extra details"


@patch("celery_cloud.runners.aws_lambda.settings")
def test_lambda_handler_generic_exception(mock_settings):
    with patch("celery_cloud.runners.aws_lambda.SQSEvent.from_lambda") as mock_from_lambda:
        mock_from_lambda.side_effect = Exception("Unexpected crash")

        result = lambda_handler({"Records": [{}]}, context={})

        assert result["status"] == "error"
        assert "General error" in result["message"]
        assert "Unexpected crash" in result["details"]


# @patch("celery_cloud.runners.aws_lambda.settings")
# @patch("celery_cloud.runners.aws_lambda.SQSEvent.from_lambda")
# def test_lambda_handler_message_decode_error(mock_from_lambda, mock_settings):
#     from celery_cloud.exceptions import MessageDecodeException
#     from celery_cloud.entities import SQSRecord, SQSEvent

#     mock_record = MagicMock(spec=SQSRecord)
#     mock_record.messageId = "msg-1"  # ✅ Necesario para el manejo de errores
#     mock_record.get_message.side_effect = MessageDecodeException("Invalid message")

#     mock_event = SQSEvent(Records=[mock_record])
#     mock_from_lambda.return_value = mock_event

#     result = lambda_handler({"Records": [{}]}, context={})

#     assert result["status"] == "error"
#     assert "Invalid message" in result["message"]
