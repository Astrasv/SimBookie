from src.interface.orderbook_parent import AbstractOrderBook
from src.models.order import Order
from src.implementations.price_level import PriceLevel

import bisect
from typing import Optional

class OrderBook(AbstractOrderBook):
    __slots__ = ()

    def add_order(
        self, order_id: int, side: str, price: float, size: float, timestamp: float
    ) -> None:

        if order_id in self.orders:
            raise ValueError(f"Order {order_id} already exists.")

        order = Order(
            order_id=order_id, side=side, price=price, size=size, timestamp=timestamp
        )
        self.orders[order_id] = order

        if side == "buy":
            if price not in self.bid_levels:
                self.bid_levels[price] = PriceLevel(price)
                idx = bisect.bisect_left(self.bid_prices, -price)
                self.bid_prices.insert(idx, -price)
            self.bid_levels[price].append(order)
        else:
            if price not in self.ask_levels:
                self.ask_levels[price] = PriceLevel(price)
                idx = bisect.bisect_right(self.ask_prices, price)
                self.ask_prices.insert(idx, price)
            self.ask_levels[price].append(order)

    def cancel_order(self, order_id: int) -> Optional[Order]:
        order = self.orders.get(order_id)
        if not order:
            return None

        del self.orders[order_id]

        if order.side == "buy":
            level = self.bid_levels.get(order.price)
            if level:
                level.remove(order)
                if level.is_empty():
                    del self.bid_levels[order.price]
                    idx = bisect.bisect_left(self.bid_prices, -order.price)
                    if (
                        idx < len(self.bid_prices)
                        and self.bid_prices[idx] == -order.price
                    ):
                        self.bid_prices.pop(idx)
        else:
            level = self.ask_levels.get(order.price)
            if level:
                level.remove(order)
                if level.is_empty():
                    del self.ask_levels[order.price]
                    idx = bisect.bisect_right(self.ask_prices, order.price)
                    if idx > 0 and self.ask_prices[idx - 1] == order.price:
                        self.ask_prices.pop(idx - 1)

        return order

    def get_best_bid(self) -> Optional[tuple[float, float]]:
        if not self.bid_prices:
            return None
        price = -self.bid_prices[0]
        return price, self.bid_levels[price].total_size

    def get_best_ask(self) -> Optional[tuple[float, float]]:
        if not self.ask_prices:
            return None
        price = self.ask_prices[0]
        return price, self.ask_levels[price].total_size
