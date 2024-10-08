import pytest
from src.factory import TaskAndSchedulerFactory
from src.scheduler import (
    FIFOTaskScheduler,
    PriorityTaskScheduler,
    RoundRobinTaskScheduler,
)
from src.tasks import Task, PriorityTask, PausableTask
from src.view import UserOptions
from src.mock import mock_task_quick, fibonacci


@pytest.fixture(autouse=True)
def setup_and_teardown():
    UserOptions.num_workers = 5
    yield
    UserOptions.type = None
    UserOptions.num_workers = None


@pytest.fixture
def fifo_scheduler_option():
    UserOptions.type = 1


@pytest.fixture
def priority_scheduler_option():
    UserOptions.type = 2


@pytest.fixture
def round_robin_scheduler_option():
    UserOptions.type = 3


@pytest.fixture
def mock_task():
    return mock_task_quick


def test_get_fifo_scheduler(fifo_scheduler_option):
    scheduler = TaskAndSchedulerFactory.get_scheduler()
    assert isinstance(scheduler, FIFOTaskScheduler)


def test_get_priority_scheduler(priority_scheduler_option):
    UserOptions.type = 2
    scheduler = TaskAndSchedulerFactory.get_scheduler()
    assert isinstance(scheduler, PriorityTaskScheduler)


def test_get_round_robin_scheduler(round_robin_scheduler_option):
    UserOptions.type = 3
    scheduler = TaskAndSchedulerFactory.get_scheduler()
    assert isinstance(scheduler, RoundRobinTaskScheduler)


def test_get_task(mock_task, fifo_scheduler_option):
    task = TaskAndSchedulerFactory.get_task(id=1, task=mock_task)
    assert isinstance(task, Task)


def test_get_priority_task(mock_task, priority_scheduler_option):
    task = TaskAndSchedulerFactory.get_task(id=1, task=mock_task, priority=1)
    assert isinstance(task, PriorityTask)


def test_get_pausable_task(mock_task, round_robin_scheduler_option):
    task = TaskAndSchedulerFactory.get_task(
        id=1, task=mock_task, gen=fibonacci(), n=1000
    )
    assert isinstance(task, PausableTask)
