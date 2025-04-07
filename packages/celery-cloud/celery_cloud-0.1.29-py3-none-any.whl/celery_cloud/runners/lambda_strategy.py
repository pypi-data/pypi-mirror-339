import boto3
import json
from typing import Any
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
import pybreaker

from celery_cloud.entities import Task, TaskRoute
from celery_cloud.exceptions import TaskExecutionException
from celery_cloud.runners.task_execution_strategy import TaskExecutionStrategy
from celery_cloud.settings import settings


# Global Circuit Breaker global with settings from configuration
breaker = pybreaker.CircuitBreaker(
    fail_max=settings.CB_FAIL_MAX,
    reset_timeout=settings.CB_RESET_TIMEOUT,
)

class LambdaTaskExecutionStrategy(TaskExecutionStrategy):
    def __init__(self):
        self.breaker = breaker

    @retry(
        stop=stop_after_attempt(settings.MAX_ATTEMPTS),
        wait=wait_exponential(multiplier=1, min=1, max=10),
        retry=retry_if_exception_type(TaskExecutionException),
        reraise=True,
    )
    def _invoke_lambda(self, lambda_client, task: Task, route: TaskRoute) -> Any:
        response = lambda_client.invoke(
            FunctionName=route.module,
            InvocationType="RequestResponse",
            Payload=json.dumps({"args": task.args, "kwargs": task.kwargs}),
        )

        response_payload = json.loads(response["Payload"].read())

        if "FunctionError" in response:
            raise TaskExecutionException(
                message=f"Lambda function {route.module} returned an error",
                detail=response_payload,
            )

        return response_payload.get("body", response_payload)

    def execute(self, task: Task, route: TaskRoute) -> Any:
        region = route.module.split(":")[3]
        lambda_client = boto3.client("lambda", region_name=region)

        try:
            # We use the breaker to wrap the lambda invocation
            # and retry on failure
            return self.breaker.call(self._invoke_lambda, lambda_client, task, route)

        except pybreaker.CircuitBreakerError as e:
            raise TaskExecutionException(
                message=f"Circuit breaker open for Lambda function {route.module}",
                detail=str(e),
            ) from e

        except TaskExecutionException:
            raise  # Re-raise the TaskExecutionException to be handled by the retry logic

        except Exception as e:
            raise TaskExecutionException(
                message=f"Unexpected error calling Lambda function {route.module}",
                detail=str(e),
            ) from e
