from src.models.order import Order
from abc import ABC, abstractmethod
from typing import Optional


class OrderQueueLevel(ABC):
    __slots__ = ('total_size', 'head', 'tail')
    
    def __init__(self):
        self.total_size: float = 0.0
        self.head: Optional[Order] = None
        self.tail: Optional[Order] = None

    @abstractmethod
    def append(self, order: Order) -> None:
        pass

    @abstractmethod
    def remove(self, order: Order) -> None:
        pass

    @abstractmethod
    def is_empty(self) -> bool:
        pass