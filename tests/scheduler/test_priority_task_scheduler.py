import pytest
from src.scheduler import PriorityTaskScheduler
from src.tasks import PriorityTask
from tests.mock import (
    mock_task_quick,
    mock_task_with_computation,
    mock_task_with_contrived_error,
    mock_task_with_random_sleep_duration,
)

MUST_BE_GREATER_THAN_ZERO = "must be greater than 0"


def test_initialize_with_valid_workers():
    with PriorityTaskScheduler(num_workers=3) as scheduler:
        assert scheduler.get_worker_count() == 3


def test_initialize_with_zero_workers():
    with pytest.raises(ValueError, match=MUST_BE_GREATER_THAN_ZERO):
        with PriorityTaskScheduler(num_workers=0):
            pass


def test_initialize_with_negative_workers():
    with pytest.raises(ValueError, match=MUST_BE_GREATER_THAN_ZERO):
        with PriorityTaskScheduler(num_workers=-1):
            pass


def test_schedule():
    with PriorityTaskScheduler(num_workers=3) as scheduler:
        mock_task = PriorityTask(id=1, task=mock_task_quick, priority=1)
        scheduler.schedule(mock_task)

        assert scheduler.get_waiting_task_count() == 1


@pytest.mark.parametrize("num_test_workers", list(range(1, 6, 2)))
def test_priority_order(num_test_workers: int):
    """Asserts that tasks with higher priorities are popped from the queue first."""

    mock_tasks = [
        PriorityTask(id=1, task=mock_task_quick, priority=3),
        PriorityTask(id=2, task=mock_task_with_computation, priority=4),
        PriorityTask(id=3, task=mock_task_with_contrived_error, priority=1),
        PriorityTask(id=4, task=mock_task_with_random_sleep_duration, priority=2),
    ]

    with PriorityTaskScheduler(
        num_workers=num_test_workers, tasks=mock_tasks
    ) as scheduler:
        scheduler.stop()
        assert scheduler.empty()

        popped_tasks = scheduler.get_popped_tasks()
        assert [task.get_priority() for task in popped_tasks] == [1, 2, 3, 4]
