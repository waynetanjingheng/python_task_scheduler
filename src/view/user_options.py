from dataclasses import dataclass
from typing import ClassVar
import logging

LOG = logging.getLogger(__name__)


@dataclass
class UserOptions:
    type: ClassVar[int]
    num_workers: ClassVar[int]
    num_tasks: ClassVar[int]
    time_quantum_ms: ClassVar[int]

    @classmethod
    def display_options_and_accept_input(cls):
        from src.factory import TaskAndSchedulerFactory

        NUM_SCHEDULING_ALGORITHMS = TaskAndSchedulerFactory.get_num_types()
        LOG.info(
            f"Number of scheduling algorithms available: {NUM_SCHEDULING_ALGORITHMS}"
        )

        print("=====================")
        for type_number, name in TaskAndSchedulerFactory.get_options():
            print(f"{type_number}: {name}")
        print("=====================\n")

        try:
            # Select scheduler type
            type_ = int(input("Welcome! Please select a scheduling algorithm: "))
            LOG.info("Type chosen: %d", type_)
            if type_ < 1 or type_ > NUM_SCHEDULING_ALGORITHMS:
                raise ValueError("Unknown type!")
            cls.type = type_

            # For Round Robin: Select time quantum
            if type_ == 3:
                time_quantum_ms = int(
                    input("Please select the scheduler time quantum in milliseconds: ")
                )
                LOG.info("Time Quantim chosen: %d", time_quantum_ms)
                if time_quantum_ms <= 0:
                    raise ValueError("Time Quantum cannot be non-positive!")
                cls.time_quantum_ms = time_quantum_ms

            # Select number of worker threads in scheduler
            num_workers = int(
                input("Please input the number of worker threads in the scheduler: ")
            )
            LOG.info("Number of worker threads chosen: %d", num_workers)
            if num_workers <= 0:
                raise ValueError("Cannot have <= 0 worker threads!")
            cls.num_workers = num_workers

            # Select number of tasks to schedule
            num_tasks = int(
                input("Please input the number of tasks you wish to schedule: ")
            )
            LOG.info(f"Number of tasks chosen: {num_tasks}")
            if num_tasks <= 0:
                raise ValueError("Cannot have <= 0 tasks!")
            cls.num_tasks = num_tasks

            print("Awesome! Initializing the scheduler...\n")

        except ValueError as e:
            LOG.error(f"Input error: {e}")
            raise
