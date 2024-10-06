from src.mixins.protocols import SupportsPriority
import functools
from dataclasses import dataclass


@dataclass
@functools.total_ordering
class PriorityMixin:
    priority: int

    def get_priority(self) -> int:
        return self.priority

    def __lt__(self, other: SupportsPriority) -> bool:
        return self.priority < other.priority

    def __eq__(self, other: SupportsPriority) -> bool:
        return self.priority == other.priority
