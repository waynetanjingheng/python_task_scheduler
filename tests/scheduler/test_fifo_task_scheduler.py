import pytest
from src.scheduler import FIFOTaskScheduler
from src.tasks import Task
from src.mock import (
    mock_task_quick,
    mock_task_with_computation,
    mock_task_with_contrived_error,
    mock_task_with_random_sleep_duration,
)

MUST_BE_GREATER_THAN_ZERO = "must be greater than 0"


def test_initialize_with_valid_workers():
    with FIFOTaskScheduler(num_workers=3) as scheduler:
        assert scheduler.get_worker_count() == 3


def test_initialize_with_zero_workers():
    with pytest.raises(ValueError, match=MUST_BE_GREATER_THAN_ZERO):
        with FIFOTaskScheduler(num_workers=0):
            pass


def test_initialize_with_negative_workers():
    with pytest.raises(ValueError, match=MUST_BE_GREATER_THAN_ZERO):
        with FIFOTaskScheduler(num_workers=-1):
            pass


def test_schedule():
    with FIFOTaskScheduler(num_workers=3) as scheduler:
        mock_task = Task(id=1, task=mock_task_quick)
        scheduler.schedule(mock_task)

        assert scheduler.get_waiting_task_count() == 1


@pytest.mark.parametrize("num_test_workers", list(range(1, 6, 2)))
def test_fifo_order(num_test_workers: int):
    mock_tasks = [
        Task(id=1, task=mock_task_quick),
        Task(id=2, task=mock_task_with_computation),
        Task(id=3, task=mock_task_with_contrived_error),
        Task(id=4, task=mock_task_with_random_sleep_duration),
    ]

    with FIFOTaskScheduler(num_workers=num_test_workers, tasks=mock_tasks) as scheduler:
        scheduler.stop()
        assert scheduler.empty()

        popped_tasks = scheduler.get_popped_tasks()
        assert [task.get_id() for task in popped_tasks] == [1, 2, 3, 4]
