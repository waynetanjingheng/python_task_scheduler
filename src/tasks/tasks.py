from typing import Callable
import logging
from dataclasses import dataclass
from src.mixins import PriorityMixin


LOG = logging.getLogger(__name__)


@dataclass
class Task:
    id: int
    task: Callable[[int], None]

    def get_id(self) -> int:
        return self.id

    def execute(self) -> None:
        if self.task is None:
            raise ValueError(
                f"Task with id: [{self.id}] cannot be executed because it's task is None!"
            )

        LOG.info(f"Executing Task with id: [{self.id}]")
        self.task(self.id)


class PriorityTask(PriorityMixin, Task):
    def __init__(self, priority: int, *args, **kwargs) -> None:
        super().__init__(priority, *args, **kwargs)
