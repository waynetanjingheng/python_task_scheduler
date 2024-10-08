from src.scheduler import (
    FIFOTaskScheduler,
    PriorityTaskScheduler,
    RoundRobinTaskScheduler,
)
from src.tasks import Task, PriorityTask, PausableTask
from src.view import UserOptions


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
    def get_scheduler(cls, type: int):
        return cls.SCHEDULER_TASK_MAP[type][1](UserOptions.num_workers)

    @classmethod
    def get_task(cls, type: int, *args, **kwargs):
        return cls.SCHEDULER_TASK_MAP[type][2](*args, **kwargs)
