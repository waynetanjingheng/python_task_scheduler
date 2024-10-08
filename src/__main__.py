import logging
from src.view import UserOptions
from src.factory import TaskAndSchedulerFactory
import time
import random

LOG = logging.getLogger("src")


def main() -> None:
    LOG.info("Starting Program...")

    UserOptions.display_options_and_accept_input()

    # Mock tasks for demo purposes
    tasks = TaskAndSchedulerFactory.get_all_tasks()

    # # Example usage 1: Initialize scheduler with a list of tasks
    # with TaskAndSchedulerFactory.get_scheduler(tasks=tasks) as scheduler:
    #     pass

    # Example usage 2: Initialize an empty scheduler, and periodically schedule tasks
    with TaskAndSchedulerFactory.get_scheduler() as scheduler:
        for task in tasks:
            scheduler.schedule(task)

            time.sleep(random.randint(1, 10) / 1000)

    LOG.info("Program exiting!")


if __name__ == "__main__":
    main()
