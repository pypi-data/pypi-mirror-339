import pytest
import json
from unittest.mock import patch, MagicMock
from celery_cloud.runners.lambda_strategy import LambdaTaskExecutionStrategy
from celery_cloud.entities import Task, TaskRoute
from celery_cloud.exceptions import TaskExecutionException
from pybreaker import CircuitBreakerError
from tenacity import RetryError


@pytest.fixture
def sample_task_and_route():
    task = Task(id="abc123", task="test.task", args=[], kwargs={})
    route = TaskRoute(
        scheme="lambda",
        module="arn:aws:lambda:us-east-1:123456:function:test-fn",
        function="",
        query={},
    )
    return task, route


@patch("celery_cloud.runners.lambda_strategy.settings")
@patch("celery_cloud.runners.lambda_strategy.breaker")
def test_lambda_strategy_circuit_breaker_open(mock_breaker, mock_settings, sample_task_and_route):
    mock_settings.MAX_ATTEMPTS = 3
    mock_settings.CB_FAIL_MAX = 5
    mock_settings.CB_RESET_TIMEOUT = 60

    # Simular que el breaker está abierto
    mock_breaker.call.side_effect = CircuitBreakerError("Circuit is open")

    strategy = LambdaTaskExecutionStrategy()
    task, route = sample_task_and_route

    with pytest.raises(TaskExecutionException) as exc:
        strategy.execute(task, route)

    assert "Circuit is open" in exc.value.detail
    assert "Circuit breaker open for Lambda function" in exc.value.message


@patch("celery_cloud.runners.lambda_strategy.settings")
@patch("celery_cloud.runners.lambda_strategy.breaker")
@patch("celery_cloud.runners.lambda_strategy.boto3.client")
def test_lambda_strategy_retry_exhausted(mock_boto_client, mock_breaker, mock_settings, sample_task_and_route):
    from tenacity import RetryError
    from tenacity import stop_after_attempt, retry

    mock_settings.MAX_ATTEMPTS = 2
    mock_settings.CB_FAIL_MAX = 5
    mock_settings.CB_RESET_TIMEOUT = 60

    # Simular error permanente en el invoke que nunca se recupera
    def always_fail_invoke(*args, **kwargs):
        raise Exception("Permanent failure")

    mock_lambda = MagicMock()
    mock_lambda.invoke.side_effect = always_fail_invoke
    mock_boto_client.return_value = mock_lambda

    def pass_through_call(fn, *args, **kwargs):
        return fn(*args, **kwargs)

    mock_breaker.call.side_effect = pass_through_call

    strategy = LambdaTaskExecutionStrategy()
    task, route = sample_task_and_route

    with pytest.raises(TaskExecutionException) as exc:
        strategy.execute(task, route)

    assert "RetryError" in exc.value.detail or "Permanent failure" in exc.value.detail
    assert "Unexpected error calling Lambda function" in exc.value.message

@patch("celery_cloud.runners.lambda_strategy.retry", lambda *a, **kw: (lambda f: f))
@patch("celery_cloud.runners.lambda_strategy.settings")
@patch("celery_cloud.runners.lambda_strategy.boto3.client")
@patch("celery_cloud.runners.lambda_strategy.breaker")  # evita que falle por el estado del breaker
def test_lambda_strategy_success(mock_breaker, mock_boto_client, mock_settings):
    # Configurar settings
    mock_settings.MAX_ATTEMPTS = 3
    mock_settings.CB_FAIL_MAX = 5
    mock_settings.CB_RESET_TIMEOUT = 60

    # Simular respuesta exitosa
    mock_lambda = MagicMock()
    mock_lambda.invoke.return_value = {
        "Payload": MagicMock(read=lambda: json.dumps({"body": "ok"}).encode())
    }
    mock_boto_client.return_value = mock_lambda

    # El breaker debe simplemente ejecutar el método directamente
    def pass_through_call(fn, *args, **kwargs):
        return fn(*args, **kwargs)

    mock_breaker.call.side_effect = pass_through_call

    strategy = LambdaTaskExecutionStrategy()
    task = Task(id="abc", task="t", args=["x"], kwargs={"y": 1})
    route = TaskRoute(
        scheme="lambda",
        module="arn:aws:lambda:us-east-1:123456:function:my-fn",
        function="",
        query={},
    )

    result = strategy.execute(task, route)
    assert result == "ok"
    mock_lambda.invoke.assert_called_once()


@patch("celery_cloud.runners.lambda_strategy.retry", lambda *a, **kw: (lambda f: f))
@patch("celery_cloud.runners.lambda_strategy.settings")
@patch("celery_cloud.runners.lambda_strategy.boto3.client")
@patch("celery_cloud.runners.lambda_strategy.breaker")
def test_lambda_strategy_with_error_response(mock_breaker, mock_boto_client, mock_settings):
    mock_settings.MAX_ATTEMPTS = 3  # Aun así puedes dejarlo
    mock_settings.CB_FAIL_MAX = 5
    mock_settings.CB_RESET_TIMEOUT = 60

    # Simular respuesta con error
    mock_lambda = MagicMock()
    mock_lambda.invoke.return_value = {
        "FunctionError": "Handled",
        "Payload": MagicMock(read=lambda: json.dumps({"error": "fail"}).encode())
    }
    mock_boto_client.return_value = mock_lambda

    def pass_through_call(fn, *args, **kwargs):
        return fn(*args, **kwargs)

    mock_breaker.call.side_effect = pass_through_call

    strategy = LambdaTaskExecutionStrategy()
    task = Task(id="abc", task="t", args=[], kwargs={})
    route = TaskRoute(
        scheme="lambda",
        module="arn:aws:lambda:us-east-1:123456:function:bad-fn",
        function="",
        query={},
    )

    with pytest.raises(TaskExecutionException) as exc:
        strategy.execute(task, route)

    assert "Lambda function" in exc.value.message
    assert "returned an error" in exc.value.message