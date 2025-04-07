import ast
import json
from typing import Any

import boto3
from ksuid import Ksuid
from pydantic import ValidationError

from celery_cloud.entities import (
    Task,
    FailedTask,
    LambdaResponse,
    ProcessedTask,
    SQSEvent,
    SQSMessage,
    SQSRecord,
    TaskRoute,
)
from celery_cloud.exceptions import (
    BackendException,
    EventDecodeException,
    MessageDecodeException,
    TaskDecodeException,
    TaskExecutionException,
)
from celery_cloud.logging import logger, trace_id_context
from celery_cloud.models.task_model import TaskModel
from celery_cloud.settings import settings
from .task_executor import TaskExecutor




def call_task(task: Task) -> Any:
    """Execute a Celery task and return the result"""
    try:
        task_config = settings.TASKS[task.task]
        route = TaskRoute.from_url(task_config)

        executor = TaskExecutor()
        task_result = executor.execute(task, route)

        logger.debug(f"Executed task: {task.task} with ID {task.id}")
        return task_result

    except Exception as e:
        logger.error(f"Exception executing task {task.id}: {str(e)}")
        raise TaskExecutionException(
            message=f"Exception executing task {task.id}", detail=str(e)
        ) from e





def lambda_handler(event: dict[str, Any], context: Any) -> dict[str, Any]:
    """Lambda handler for processing Celery Broker events

    Args:
        event (dict[str, Any]): _description_
        context (Any): _description_

    Returns:
        dict[str, Any]: _description_
    """

    # TODO: refactor this function to make it more readable

    processed_tasks: list[ProcessedTask] = []
    failed_tasks: list[FailedTask] = []

    # Logging: Generate KSUID as trace_id
    trace_id = str(Ksuid())
    # Logging: Assign trace_id to context
    trace_id_context.set(trace_id)

    logger.debug(f"Processing lambda event: {event} with context: {context}")

    logger.debug(f"Settings TASKS: {settings.TASKS}")

    try:
        # 1. Decode the event depending on the event source
        # TODO: Only SQS managed by now, add more event types

        sqs_event: SQSEvent = SQSEvent.from_lambda(event)

        logger.debug(f"Processing lambda event: {sqs_event.model_dump()}")

        # 3. Process the event
        for record in sqs_event.Records:
            message: dict[str, Any] = record.get_message()
            # TODO: validate fields exist
            sqs_message: SQSMessage = SQSMessage(
                body=message["body"],
                content_encoding=message["content-encoding"],
                content_type=message["content-type"],
                headers=message["headers"],
                properties=message["properties"],
            )
            logger.debug(f"Processing message: {sqs_message}")

            # 3.2. Get celery Task from message
            task: Task = sqs_message.get_task()
            logger.debug(f"Processing task: {task}")

            # Set task status to "PROCESSING" in backend
            TaskModel.insert_task(task_uuid=task.id)

            # 3.3. Check if task is supported
            if task.task not in settings.TASKS:
                logger.error(f"Task '{task.task}' not supported")

                failed_tasks.append(
                    FailedTask(
                        message_id=record.messageId,
                        task_id=task.id,
                        error=f"Task '{task.task}' not supported",
                    )
                )

                # 3.3.1. Update task status and result in backend
                TaskModel.update_task(task.id, status="ERROR", result=None)

                continue

            # 3.4. Call function with args and kwargs
            task_result: Any = call_task(task)

            logger.debug(f"Processed task: {task.task} with ID {task.id}")

            # 3.5. Update task status and result in backend
            TaskModel.update_task(task.id, status="SUCCESS", result=task_result)

            # 3.6. Append task to processed tasks
            processed_tasks.append(
                ProcessedTask(
                    task_id=task.id,
                    status="SUCCESS",
                    result=task_result,
                )
            )

        # Clear context before finishing the function
        trace_id_context.set(None)

        return LambdaResponse(
            status="completed",
            processed_messages=len(processed_tasks),
            failed_messages=len(failed_tasks),
            processed_tasks=processed_tasks if processed_tasks else None,
            failed_tasks=failed_tasks if failed_tasks else None,
        ).model_dump()

    except (
        MessageDecodeException,
        TaskDecodeException,
        BackendException,
        TaskExecutionException,
    ) as e:
        failed_tasks.append(
            FailedTask(
                message_id=record.messageId,
                error=f"{str(e)}",
            )
        )

    # TODO: Add more specific error handling (Exception) to capture all errors
    except EventDecodeException as e:
        # Clear context before finishing the function
        trace_id_context.set(None)

        return LambdaResponse(
            status="error",
            message=e.message,
            details=e.detail,
        ).model_dump()

    except Exception as e:
        # Clear context before finishing the function
        trace_id_context.set(None)

        return LambdaResponse(
            status="error",
            message=f"General error: {str(e)}",
            details=str(e),
        ).model_dump()
