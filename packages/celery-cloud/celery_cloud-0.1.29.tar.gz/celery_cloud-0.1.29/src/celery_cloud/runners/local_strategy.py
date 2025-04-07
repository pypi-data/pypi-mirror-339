from celery_cloud.entities import Task, TaskRoute
from typing import Any

from celery_cloud.runners.task_execution_strategy import TaskExecutionStrategy
from celery_cloud.logging import logger

class LocalTaskExecutionStrategy(TaskExecutionStrategy):
    def execute(self, task: Task, route: TaskRoute) -> Any:

        logger.debug(f"Executing task {task.task} with args: {task.args} and kwargs: {task.kwargs}")

        module = __import__(route.module, fromlist=[route.function])
        function = getattr(module, route.function)

        logger.debug(f"Function {function} imported from module {route.module}")

        return function(task.args, task.kwargs)
