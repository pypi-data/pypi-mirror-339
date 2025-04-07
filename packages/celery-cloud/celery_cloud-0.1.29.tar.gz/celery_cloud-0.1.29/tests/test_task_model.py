import pytest
from unittest.mock import patch, MagicMock
import json
import base64
from celery_cloud.models.task_model import TaskModel
from celery_cloud.exceptions import BackendException


@patch("celery_cloud.models.task_model.TaskModel.save")
@patch("celery_cloud.models.task_model.settings")
def test_insert_task_success(mock_settings, mock_save):
    mock_settings.CELERY_BACKEND_TABLE = "table"
    mock_settings.CELERY_BACKEND_REGION = "region"

    task_uuid = "abc123"
    task = TaskModel.insert_task(task_uuid)

    assert task.id == str(f"celery-task-meta-{task_uuid}".encode())
    assert isinstance(task.result, bytes)


@patch("celery_cloud.models.task_model.TaskModel.save", side_effect=Exception("DB error"))
@patch("celery_cloud.models.task_model.settings")
def test_insert_task_error(mock_settings, mock_save):
    mock_settings.CELERY_BACKEND_TABLE = "table"
    mock_settings.CELERY_BACKEND_REGION = "region"

    with pytest.raises(BackendException) as exc:
        TaskModel.insert_task("abc123")
    assert "Error inserting task" in str(exc.value)


@patch("celery_cloud.models.task_model.TaskModel.get")
@patch("celery_cloud.models.task_model.TaskModel.update")
def test_update_task_success(mock_update, mock_get):
    mock_task = MagicMock()
    mock_get.return_value = mock_task

    task = TaskModel.update_task("abc123", "SUCCESS", result={"value": 42})
    assert task == mock_task


@patch("celery_cloud.models.task_model.TaskModel.get", side_effect=TaskModel.DoesNotExist)
def test_update_task_does_not_exist(mock_get):
    assert TaskModel.update_task("missing-id", "SUCCESS") is None


@patch("celery_cloud.models.task_model.TaskModel.get", side_effect=Exception("Boom"))
def test_update_task_error(mock_get):
    with pytest.raises(BackendException) as exc:
        TaskModel.update_task("abc123", "FAILURE")
    assert "Error updating task" in str(exc.value)


@patch("celery_cloud.models.task_model.TaskModel.get")
def test_get_task_success(mock_get):
    encoded = base64.b64encode(json.dumps({"status": "SUCCESS"}).encode())
    mock_task = MagicMock(result=encoded, timestamp=123456.0)
    mock_get.return_value = mock_task

    task_data = TaskModel.get_task("abc123")
    assert task_data["result"]["status"] == "SUCCESS"
    assert task_data["timestamp"] == 123456.0


@patch("celery_cloud.models.task_model.TaskModel.get", side_effect=TaskModel.DoesNotExist)
def test_get_task_does_not_exist(mock_get):
    assert TaskModel.get_task("unknown") is None


@patch("celery_cloud.models.task_model.TaskModel.get", side_effect=Exception("Oops"))
def test_get_task_error(mock_get):
    with pytest.raises(BackendException) as exc:
        TaskModel.get_task("abc123")
    assert "Error getting task" in str(exc.value)
