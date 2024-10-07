from dataclasses import dataclass


@dataclass(order=True)
class PriorityMixin:
    priority: int

    def get_priority(self) -> int:
        return self.priority
