from src.tasks import Task
from .mock_functions import (
    mock_task_with_random_sleep_duration,
    mock_task_with_computation,
    mock_task_with_contrived_error,
    mock_task_quick,
)


def test_mock_task_with_random_sleep_duration():
    task = Task(id=1, task=mock_task_with_random_sleep_duration)
    task.execute()


def test_mock_task_with_computation():
    task = Task(id=2, task=mock_task_with_computation)
    task.execute()


def test_mock_task_with_contrived_error():
    task = Task(id=3, task=mock_task_with_contrived_error)
    task.execute()


def test_mock_task_quick():
    task = Task(id=4, task=mock_task_quick)
    task.execute()
