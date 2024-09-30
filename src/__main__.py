import logging
from src.scheduler import TaskScheduler

LOG = logging.getLogger("src")


def main() -> None:
    LOG.info("Starting Program...")

    with TaskScheduler(4) as task_scheduler:
        LOG.info("In task scheduler. Should not exit yet.")

    LOG.info("Program exiting!")


if __name__ == "__main__":
    main()
