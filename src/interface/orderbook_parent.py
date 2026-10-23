from abc import ABC, abstractmethod
from typing import Dict, List, Optional
from src.models.order import Order
from src.implementations.price_level import PriceLevel
# from typing import list, Dict


class AbstractOrderBook(ABC):
    __slots__ = ('orders', 'bid_levels', 'ask_levels', 'bid_prices', 'ask_prices')

    def __init__(self):
        self.orders: Dict[int, Order] = {}
        self.bid_levels: Dict[float, PriceLevel] = {}
        self.ask_levels: Dict[float, PriceLevel] = {}
        self.bid_prices: List[float] = []  # TO ME: make sure to store -ve for maxheap
        self.ask_prices: List[float] = [] 

    @abstractmethod
    def add_order(self, order_id: int, side: str, price: float, size: float, timestamp: float) -> None: pass

    @abstractmethod
    def cancel_order(self, order_id: int) -> Optional[Order]:pass

    @abstractmethod
    def get_best_bid(self) -> Optional[tuple[float, float]]:pass

    @abstractmethod
    def get_best_ask(self) -> Optional[tuple[float, float]]:pass

    @abstractmethod
    def execute_market_order(self, side: str, size: float) -> list[dict]: pass