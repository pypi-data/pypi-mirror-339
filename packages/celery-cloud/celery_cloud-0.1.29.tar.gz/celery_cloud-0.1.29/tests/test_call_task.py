import pytest
from unittest.mock import patch, MagicMock
from celery_cloud.runners.aws_lambda import call_task
from celery_cloud.entities import Task, TaskRoute
from celery_cloud.exceptions import TaskExecutionException

# =============================
# Test: call_task con estrategia "task" (local)
# =============================
@patch("celery_cloud.runners.aws_lambda.settings")
@patch("celery_cloud.runners.aws_lambda.TaskRoute")
@patch("celery_cloud.runners.task_executor.LocalTaskExecutionStrategy.execute")
def test_call_task_local_success(mock_local_execute, mock_taskroute, mock_settings):
    mock_settings.TASKS = {"my.task": "task://my_module/my_function"}

    fake_route = MagicMock()
    fake_route.scheme = "task"
    mock_taskroute.from_url.return_value = fake_route

    mock_local_execute.return_value = "local_result"

    task = Task(id="abc", task="my.task", args=[], kwargs={})
    result = call_task(task)

    assert result == "local_result"
    mock_local_execute.assert_called_once_with(task, fake_route)

# =============================
# Test: call_task con estrategia "lambda"
# =============================
@patch("celery_cloud.runners.aws_lambda.settings")
@patch("celery_cloud.runners.aws_lambda.TaskRoute")
@patch("celery_cloud.runners.task_executor.LambdaTaskExecutionStrategy.execute")
def test_call_task_lambda_success(mock_lambda_execute, mock_taskroute, mock_settings):
    mock_settings.TASKS = {"my.task": "lambda://aws:lambda:us-east-1:function/my-fn"}

    fake_route = MagicMock()
    fake_route.scheme = "lambda"
    mock_taskroute.from_url.return_value = fake_route

    mock_lambda_execute.return_value = {"status": "ok"}

    task = Task(id="abc", task="my.task", args=[], kwargs={})
    result = call_task(task)

    assert result == {"status": "ok"}
    mock_lambda_execute.assert_called_once_with(task, fake_route)

# =============================
# Test: call_task con esquema inválido
# =============================
@patch("celery_cloud.runners.aws_lambda.settings")
@patch("celery_cloud.runners.aws_lambda.TaskRoute")
def test_call_task_invalid_scheme(mock_taskroute, mock_settings):
    mock_settings.TASKS = {"my.task": "ftp://bad.scheme.com"}
    fake_route = MagicMock()
    fake_route.scheme = "ftp"
    mock_taskroute.from_url.return_value = fake_route

    task = Task(id="abc", task="my.task", args=[], kwargs={})

    with pytest.raises(TaskExecutionException) as exc:
        call_task(task)

    assert "Unsupported task scheme" in str(exc.value.detail)

# =============================
# Test: call_task con error inesperado en estrategia
# =============================
@patch("celery_cloud.runners.aws_lambda.settings")
@patch("celery_cloud.runners.aws_lambda.TaskRoute")
@patch("celery_cloud.runners.task_executor.LocalTaskExecutionStrategy.execute")
def test_call_task_raises_generic_error(mock_local_execute, mock_taskroute, mock_settings):
    mock_settings.TASKS = {"my.task": "task://broken.module/fn"}
    fake_route = MagicMock()
    fake_route.scheme = "task"
    mock_taskroute.from_url.return_value = fake_route

    mock_local_execute.side_effect = RuntimeError("Boom")

    task = Task(id="abc", task="my.task", args=[], kwargs={})

    with pytest.raises(TaskExecutionException) as exc:
        call_task(task)

    assert "Exception executing task abc" in exc.value.message
    assert "Boom" in exc.value.detail
