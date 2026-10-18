import random

from src.implementations.order_book import OrderBook
from src.interface.agent import Agent


class ZeroIntelligenceAgent(Agent):
    def __init__(self, agent_id: int, symbol_tick_size: float = 0.01):
        super().__init__(agent_id)
        self.tick_size = symbol_tick_size

    def generate_action(self, book: OrderBook, current_time: float):
        # Determine action type:
        #  0 = Limit Order
        # 1 = Cancel
        # 2 = Market-ish action
        action_type = random.choices([0, 1], weights=[0.7, 0.3])[0]

        if action_type == 0 or not book.orders:
            # Place a limit order near the mid price
            best_bid = book.get_best_bid()
            best_ask = book.get_best_ask()

            if best_bid and best_ask:
                mid_price = (best_bid[0] + best_ask[0]) / 2.0
            else:
                mid_price = 100.0  # set this a default price for time being

            side = random.choice(["buy", "sell"])

            # offset from mid price
            offset = random.choice([1, 2, 3]) * self.tick_size
            price = mid_price - offset if side == "buy" else mid_price + offset
            size = random.choice([10, 20, 50])
            order_id = random.randint(100000, 999999)

            return ("add", order_id, side, round(price, 2), size, current_time)

        else:
            if book.orders:
                random_order_id = random.choice(list(book.orders.keys()))
                return ("cancel", random_order_id)

        return None
