from typing import Callable
import logging
from dataclasses import dataclass
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
