from src.models.order import Order
from src.interface.order_queue_level import OrderQueueLevel


class PriceLevel(OrderQueueLevel):
    __slots__ = ('price',)

    def __init__(self, price: float):
        super().__init__()  
        self.price: float = price

    def append(self, order: Order) -> None:
        order.prev = self.tail
        order.next = None
        if self.tail:
            self.tail.next = order
        else:
            self.head = order
        self.tail = order
        self.total_size += order.size

    def remove(self, order: Order) -> None:
        if order.prev:
            order.prev.next = order.next
        else:
            self.head = order.next

        if order.next:
            order.next.prev = order.prev
        else:
            self.tail = order.prev

        self.total_size -= order.size
        order.prev = None
        order.next = None

    def is_empty(self) -> bool:
        return self.head is None