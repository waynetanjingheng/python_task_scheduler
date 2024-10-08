from dataclasses import dataclass
from typing import ClassVar
import logging

LOG = logging.getLogger(__name__)


@dataclass
class UserOptions:
    type: ClassVar[int]
    num_workers: ClassVar[int]
    num_tasks: ClassVar[int]

    @classmethod
    def display_options_and_accept_input(cls):
        NUM_SCHEDULING_ALGORITHMS = 3
        LOG.info(
            f"Number of scheduling algorithms available: {NUM_SCHEDULING_ALGORITHMS}"
        )

        print("Welcome! Please select a scheduling algorithm:")
        print("=====================")
        print("1: FIFO")
        print("2: Priority")
        print("3: Round Robiin")
        print("=====================\n")

        try:
            type = int(input())
            LOG.info("Type chosen: %d", type)
            if type < 1 or type > NUM_SCHEDULING_ALGORITHMS:
                raise ValueError("Unknown type!")
            cls.type = type

            print("Please input the number of worker threads in the scheduler:\n")
            num_workers = int(input())
            LOG.info("Number of worker threads chosen: %d", num_workers)
            if num_workers <= 0:
                raise ValueError("Cannot have <= 0 worker threads!")
            cls.num_workers = num_workers

            print("Please input the number of tasks you wish to schedule:\n")
            num_tasks = int(input())
            LOG.info(f"Number of tasks chosen: {num_tasks}")
            if num_tasks <= 0:
                raise ValueError("Cannot have <= 0 tasks!")
            cls.num_tasks = num_tasks

            print("Awesome! Initializing the scheduler...\n")

        except ValueError as e:
            LOG.error(f"Input error: {e}")
            raise
