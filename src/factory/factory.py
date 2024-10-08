from src.scheduler import (
    FIFOTaskScheduler,
    PriorityTaskScheduler,
    RoundRobinTaskScheduler,
)
from src.tasks import Task, PriorityTask, PausableTask
from src.view import UserOptions
from src.mock import (
    mock_task_quick,
    mock_task_with_computation,
    mock_task_with_random_sleep_duration,
    mock_task_with_contrived_error,
    fibonacci,
)


class TaskAndSchedulerFactory:
    SCHEDULER_TASK_MAP = {
        1: ["FIFO", FIFOTaskScheduler, Task],
        2: ["Priority", PriorityTaskScheduler, PriorityTask],
        3: ["Round Robin", RoundRobinTaskScheduler, PausableTask],
    }

    @classmethod
    def get_num_types(cls):
        return len(cls.SCHEDULER_TASK_MAP)

    @classmethod
    def get_options(cls):
        return [
            (type_number, value[0])
            for type_number, value in cls.SCHEDULER_TASK_MAP.items()
        ]

    @classmethod
    def get_scheduler(cls, *args, **kwargs):
        type_ = UserOptions.type
        num_workers = UserOptions.num_workers

        if type_ == 3:  # Round Robin
            kwargs["time_quantum_ms"] = UserOptions.time_quantum_ms

        return cls.SCHEDULER_TASK_MAP[type_][1](num_workers, *args, **kwargs)

    @classmethod
    def get_all_tasks(cls):
        """Generates n mock tasks for testing/demo purposes, where n is the
        number of tasks specified by the user."""
        MOCK_FUNCTIONS = [
            mock_task_quick,
            mock_task_with_computation,
            mock_task_with_contrived_error,
            mock_task_with_random_sleep_duration,
        ]

        # Since PriorityTask and PausableTask require additional args,
        # we conditionally pass them to the Task constructor.
        additional_task_args = {}
        if UserOptions.type == 3:  # Round Robin
            additional_task_args["gen"] = fibonacci()
            additional_task_args["n"] = 10**5

        tasks = []

        for i in range(UserOptions.num_tasks):
            if UserOptions.type == 2:  # Priority
                additional_task_args["priority"] = (
                    1000 - i
                )  # Make functions execute in reverse order for demo

            tasks.append(
                cls.get_task(
                    id=i + 1,
                    task=MOCK_FUNCTIONS[i % len(MOCK_FUNCTIONS)],
                    **additional_task_args
                )
            )

        return tasks

    @classmethod
    def get_task(cls, *args, **kwargs):
        type_ = UserOptions.type
        return cls.SCHEDULER_TASK_MAP[type_][2](*args, **kwargs)
