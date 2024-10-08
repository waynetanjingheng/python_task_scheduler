import pytest
from src.factory import TaskAndSchedulerFactory
from src.scheduler import (
    FIFOTaskScheduler,
    PriorityTaskScheduler,
    RoundRobinTaskScheduler,
)
from src.tasks import Task, PriorityTask, PausableTask
from src.view import UserOptions
from tests.mock import mock_task_quick, fibonacci


@pytest.fixture(autouse=True, scope="module")
def setup_and_teardown():
    UserOptions.num_workers = 5
    yield
    UserOptions.num_workers = None


@pytest.fixture
def mock_task():
    return mock_task_quick


def test_get_fifo_scheduler():
    scheduler = TaskAndSchedulerFactory.get_scheduler(1)
    assert isinstance(scheduler, FIFOTaskScheduler)


def test_get_priority_scheduler():
    scheduler = TaskAndSchedulerFactory.get_scheduler(2)
    assert isinstance(scheduler, PriorityTaskScheduler)


def test_get_round_robin_scheduler():
    scheduler = TaskAndSchedulerFactory.get_scheduler(3)
    assert isinstance(scheduler, RoundRobinTaskScheduler)


def test_get_task(mock_task):
    task = TaskAndSchedulerFactory.get_task(type=1, id=1, task=mock_task)
    assert isinstance(task, Task)


def test_get_priority_task(mock_task):
    task = TaskAndSchedulerFactory.get_task(type=2, id=1, task=mock_task, priority=1)
    assert isinstance(task, PriorityTask)


def test_get_pausable_task(mock_task):
    task = TaskAndSchedulerFactory.get_task(
        type=3, id=1, task=mock_task, gen=fibonacci(), n=1000
    )
    assert isinstance(task, PausableTask)
