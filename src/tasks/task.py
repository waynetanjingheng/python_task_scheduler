from typing import Callable
import logging

LOG = logging.getLogger(__name__)


class Task:
    def __init__(self, id: int, task: Callable[[int], None]) -> None:
        self._id = id
        self._task = task

    def get_id(self) -> int:
        return self._id

    def execute(self) -> None:
        if self._task is None:
            raise ValueError(
                f"Task with id: [{self.id}] cannot be executed because it's task is None!"
            )

        LOG.info(f"Executing Task with id: [{self.id}]")
        self._task()
