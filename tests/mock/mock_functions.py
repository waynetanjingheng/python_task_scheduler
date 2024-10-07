import logging
import random
import time
import math

LOG = logging.getLogger(__name__)


def mock_task_with_random_sleep_duration(task_id: int) -> None:
    if task_id is None:
        raise ValueError("task_id cannot be None!")

    sleep_duration = random.randint(1, 5)
    LOG.info(
        "Sleeping Task with id: [%d] started, will take %d seconds.",
        task_id,
        sleep_duration,
    )

    time.sleep(sleep_duration)
    LOG.info("Sleeping Task with id: [%d] completed. Bye!", task_id)


def mock_task_with_computation(task_id: int) -> None:
    if task_id is None:
        raise ValueError("task_id cannot be None!")

    LOG.info(
        "Computation Task with id: [%d] started some intense computation.", task_id
    )
    sum_result = 0
    bound = int(math.pow(10, 6))

    for i in range(bound):
        sum_result += i

    LOG.info(
        "Computation Task with id: [%d] completed computation with result: %d",
        task_id,
        sum_result,
    )


def mock_task_with_contrived_error(task_id: int) -> None:
    if task_id is None:
        raise ValueError("task_id cannot be None!")

    LOG.info(
        "Potentially erroneous Task with id: [%d] started, might encounter an error.",
        task_id,
    )

    try:
        if task_id % 2 == 0:
            raise RuntimeError("Contrived error in task {}".format(task_id))

        time.sleep(3)
    except Exception as e:
        LOG.error(
            "Potentially erroneous Task with id: [%d] encountered an error: %s",
            task_id,
            str(e),
        )
        return

    LOG.info(
        "Potentially erroneous Task with id: [%d] completed successfully. Yay!", task_id
    )


def mock_task_quick(task_id: int) -> None:
    if task_id is None:
        raise ValueError("task_id cannot be None!")

    LOG.info("Quick Task with id: [%d] started quick execution.", task_id)

    time.sleep(0.1)  # Sleep for 100 milliseconds
    LOG.info("Quick Task with id: [%d] completed quick execution.", task_id)


def fibonacci():
    """Generator that yields an infinite sequence of Fibonacci numbers."""
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b
