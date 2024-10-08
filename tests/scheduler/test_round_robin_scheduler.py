import pytest
from src.scheduler import RoundRobinTaskScheduler
from src.tasks import PausableTask
from src.mock import (
    fibonacci,
)

MUST_BE_GREATER_THAN_ZERO = "must be greater than 0"


def test_initialize_with_valid_workers():
    with RoundRobinTaskScheduler(num_workers=3) as scheduler:
        assert scheduler.get_worker_count() == 3


def test_initialize_with_zero_workers():
    with pytest.raises(ValueError, match=MUST_BE_GREATER_THAN_ZERO):
        with RoundRobinTaskScheduler(num_workers=0):
            pass


def test_initialize_with_negative_workers():
    with pytest.raises(ValueError, match=MUST_BE_GREATER_THAN_ZERO):
        with RoundRobinTaskScheduler(num_workers=-1):
            pass


def test_schedule():
    with RoundRobinTaskScheduler(num_workers=3) as scheduler:
        mock_task = PausableTask(id=1, gen=fibonacci(), n=10**5, task=None)
        scheduler.schedule(mock_task)

        assert scheduler.get_waiting_task_count() == 1


@pytest.mark.parametrize("num_test_workers", list(range(1, 6, 2)))
def test_round_robin_order(num_test_workers: int):
    """This test does not assert the expected execution order due to the
    non-determinism in executions per time quantum.
    Refer to logs to check correctness.
    """
    N = 10**5

    mock_tasks = [
        PausableTask(id=1, gen=fibonacci(), n=N, task=None),
        PausableTask(id=2, gen=fibonacci(), n=N, task=None),
        PausableTask(id=3, gen=fibonacci(), n=N, task=None),
        PausableTask(id=4, gen=fibonacci(), n=N, task=None),
    ]

    with RoundRobinTaskScheduler(
        num_workers=num_test_workers, tasks=mock_tasks, time_quantum_ms=20
    ) as scheduler:
        scheduler.stop()
        assert scheduler.empty()


@pytest.mark.parametrize("time_quantum_ms", list(range(10, 100, 20)))
def test_different_time_quantums(time_quantum_ms):
    N = 10**5

    mock_tasks = [
        PausableTask(id=1, gen=fibonacci(), n=N, task=None),
        PausableTask(id=2, gen=fibonacci(), n=N, task=None),
        PausableTask(id=3, gen=fibonacci(), n=N, task=None),
        PausableTask(id=4, gen=fibonacci(), n=N, task=None),
    ]

    with RoundRobinTaskScheduler(
        num_workers=4, tasks=mock_tasks, time_quantum_ms=time_quantum_ms
    ) as scheduler:
        scheduler.stop()
        assert scheduler.empty()
