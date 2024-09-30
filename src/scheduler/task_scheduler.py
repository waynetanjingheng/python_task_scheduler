import logging
from queue import Queue
from typing import Self, Optional, Type
from types import TracebackType
from src.tasks.task import Task
import threading

LOG = logging.getLogger(__name__)


class TaskScheduler:
    def __init__(self, num_workers) -> None:
        self._num_workers = num_workers
        self._workers = []
        self._tasks = Queue()
        self._stop = False
        self._cv = threading.Condition()

    def __enter__(self) -> Self:
        LOG.info("Entering TaskScheduler context...")
        self.start()
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        exc_traceback: Optional[TracebackType],
    ):
        self.wait_for_all_tasks_to_complete()
        LOG.info("Exiting TaskScheduler context...")

    def start(self) -> None:
        for _ in range(self._num_workers):
            worker = threading.Thread(target=self.execute_tasks)
            worker.start()
            self._workers.append(worker)

        LOG.info("%d worker threads initialized.", self._num_workers)

    def enqueue_task(self, task: Task) -> None:
        with self._cv:
            self._tasks.put(task)
            LOG.info("Task with id: %d enqueued.", task.get_id())
            self._cv.notify()

    def get_next(self) -> Task:
        task = self._tasks.get()
        LOG.info("Task with id: %d popped.", task.get_id())
        return task

    def execute_tasks(self) -> None:
        while True:
            LOG.info("Thread polling...")

            with self._cv:

                while not self._stop and self.empty():
                    self._cv.wait()

                if self._stop and self.empty():
                    LOG.info("Thread has finished polling.")
                    return

                task = self.get_next()
                task.execute()
                self._tasks.task_done()

    def wait_for_all_tasks_to_complete(self) -> None:
        LOG.info("Waiting for all tasks to complete...")

        with self._cv:
            self._stop = True
            self._cv.notify_all()

        self._tasks.join()

        for worker in self._workers:
            if worker.is_alive():
                worker.join()

    def empty(self) -> bool:
        return self._tasks.empty()

    def get_waiting_task_count(self) -> int:
        return self._tasks.qsize()
