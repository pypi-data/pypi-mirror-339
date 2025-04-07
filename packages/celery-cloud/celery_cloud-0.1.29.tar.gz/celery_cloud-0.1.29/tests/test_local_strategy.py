import pytest
from unittest.mock import patch, MagicMock
from celery_cloud.runners.local_strategy import LocalTaskExecutionStrategy
from celery_cloud.entities import Task, TaskRoute

@patch("builtins.__import__")
def test_local_strategy_success(mock_import):
    fake_func = MagicMock(return_value="done")
    fake_module = MagicMock()
    setattr(fake_module, "my_func", fake_func)
    mock_import.return_value = fake_module

    strategy = LocalTaskExecutionStrategy()
    task = Task(id="abc", task="t", args=[1], kwargs={"k": 2})
    route = TaskRoute(scheme="task", module="some.module", function="my_func", query={})

    result = strategy.execute(task, route)

    assert result == "done"
    fake_func.assert_called_once_with([1], {"k": 2})

@patch("builtins.__import__")
def test_local_strategy_attribute_error(mock_import):
    fake_module = MagicMock()
    del fake_module.non_existent
    mock_import.return_value = fake_module

    strategy = LocalTaskExecutionStrategy()
    task = Task(id="abc", task="t", args=[], kwargs={})
    route = TaskRoute(scheme="task", module="some.module", function="non_existent", query={})

    with pytest.raises(AttributeError):
        strategy.execute(task, route)
