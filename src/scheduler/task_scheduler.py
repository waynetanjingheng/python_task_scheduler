import logging
from queue import Queue, PriorityQueue
from typing import Self, Optional, Type, List
from types import TracebackType
from src.tasks import Task
import threading
from abc import ABC

LOG = logging.getLogger(__name__)


class BaseTaskScheduler(ABC):
    def __init__(self, num_workers: int, tasks: Optional[List[Task]] = None) -> None:
        if num_workers <= 0:
            LOG.error(
                "Attempted to initialize TaskScheduler with %d workers!", num_workers
            )
            raise ValueError(
                f"Number of worker threads must be greater than 0, but got {num_workers}!"
            )

        self._num_workers = num_workers
        self._workers = []
        self._stop = False
        self._cv = threading.Condition()
        self._popped_tasks = Queue()
        self._lock = threading.Lock()

        if tasks:
            LOG.info("%d tasks received in the constructor.", len(tasks))
            for task in tasks:
                self.schedule(task)

    def __enter__(self) -> Self:
        LOG.info("Entering TaskScheduler context...")
        self.start()
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        exc_traceback: Optional[TracebackType],
    ) -> None:
        self.stop()
        LOG.info("Exiting TaskScheduler context...")

    # ========== Public APIs ==========

    def start(self) -> None:
        for _ in range(self._num_workers):
            worker = threading.Thread(target=self.execute)
            worker.start()
            self._workers.append(worker)

        LOG.info("%d worker threads initialized.", self._num_workers)

    def stop(self) -> None:
        LOG.info("Waiting for all tasks to complete...")

        with self._cv:
            self._stop = True
            self._cv.notify_all()

        self._tasks.join()

        for worker in self._workers:
            if worker.is_alive():
                worker.join()

    def schedule(self, task: Task) -> None:
        with self._cv:
            self._tasks.put(task)
            LOG.info("Task with id: [%d] enqueued.", task.get_id())
            self._cv.notify()

    def execute(self) -> None:
        while True:
            LOG.info("Thread polling...")

            with self._cv:
                while not self._stop and self.empty():
                    self._cv.wait()

                if self._stop and self.empty():
                    LOG.info("Thread has finished polling.")
                    return

                task = self._pop()
                task.execute()
                self._tasks.task_done()

    def empty(self) -> bool:
        return self._tasks.empty()

    def get_waiting_task_count(self) -> int:
        return self._tasks.qsize()

    def get_worker_count(self) -> int:
        return len(self._workers)

    def get_popped_tasks(self) -> List[Task]:
        """Returns a list of tasks in the order they were popped from the queue."""
        tasks = []

        # A lock ensures that other threads calling self._pop() does not mutate the Queue
        # while this method is executing.
        with self._lock:
            while not self._popped_tasks.empty():
                task = self._popped_tasks.get()
                tasks.append(task)

            for task in tasks:
                self._popped_tasks.put(task)

        return tasks

    # ========== Private APIs (for internal usage) ==========

    def _pop(self) -> Task:
        task = self._tasks.get()
        LOG.info("Task with id: [%d] popped.", task.get_id())

        with self._lock:
            self._popped_tasks.put(task)

        return task


class FIFOTaskScheduler(BaseTaskScheduler):
    def __init__(self, num_workers: int, tasks: Optional[List[Task]] = None) -> None:
        self._tasks = Queue()
        super().__init__(num_workers=num_workers, tasks=tasks)


class PriorityTaskScheduler(BaseTaskScheduler):
    def __init__(self, num_workers: int, tasks: Optional[List[Task]] = None) -> None:
        self._tasks = PriorityQueue()
        super().__init__(num_workers=num_workers, tasks=tasks)
