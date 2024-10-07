from typing import Callable
import logging
from dataclasses import dataclass, field
from src.mixins import PriorityMixin


LOG = logging.getLogger(__name__)


@dataclass
class Task:
    id: int
    task: Callable[[int], None]

    def __post_init__(self) -> None:
        LOG.info(
            "Task created with id: [%d]",
            self.id,
        )

    def get_id(self) -> int:
        return self.id

    def execute(self) -> None:
        if self.task is None:
            raise ValueError(
                f"Task with id: [{self.id}] cannot be executed because it's task is None!"
            )

        LOG.info("Executing Task with id: [%d]", self.id)
        self.task(self.id)


@dataclass
class PriorityTask(PriorityMixin, Task):
    def __post_init__(self) -> None:
        LOG.info(
            "PriorityTask created with priority: [%d] and id: [%d]",
            self.priority,
            self.id,
        )


@dataclass
class PausableTask(Task):
    gen: iter
    n: int
    running: bool = field(default=False)

    def __post_init__(self) -> None:
        LOG.info(
            "PausableTask created with n: [%d] and id: [%d]",
            self.n,
            self.id,
        )

    def get_running(self) -> bool:
        return self.running

    def completed(self) -> bool:
        return self.n == 0

    def execute(self) -> None:
        self.running = True

        while self.running and self.n > 0:
            next(self.gen)
            self.n -= 1

        if not self.running:
            LOG.info(
                "Execution paused in PausableTask with id: [%d]! self.n is: [%d]",
                self.id,
                self.n,
            )
        else:
            LOG.info("PausableTask with id: [%d] ended!", self.id)

    def pause(self) -> None:
        self.running = False
