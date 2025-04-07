from celery_cloud.entities import Task, TaskRoute
from celery_cloud.exceptions import TaskExecutionException
from typing import Any
from celery_cloud.logging import logger, trace_id_context
from .lambda_strategy import LambdaTaskExecutionStrategy
from .local_strategy import LocalTaskExecutionStrategy


class TaskExecutor:
    def __init__(self):
        self.strategies = {
            "lambda": LambdaTaskExecutionStrategy(),
            "task": LocalTaskExecutionStrategy(),
        }

    def execute(self, task: Task, route: TaskRoute) -> Any:
        logger.debug(
            f"Executing task {task.task} with ID {task.id} using route {route}"
        )
        strategy = self.strategies.get(route.scheme)

        logger.debug(
            f"Using strategy {strategy} for task {task.task} with ID {task.id}"
        )

        if not strategy:
            raise TaskExecutionException(
                message=f"Unsupported task scheme: {route.scheme}",
                detail=route.scheme,
            )
        return strategy.execute(task, route)
