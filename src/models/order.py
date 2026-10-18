from dataclasses import dataclass
from typing import Optional


@dataclass(slots=True)
class Order:
    order_id: int
    side: str  # 'buy' or 'sell'
    price: float
    size: float
    timestamp: float
    prev: Optional["Order"] = None
    next: Optional["Order"] = None
