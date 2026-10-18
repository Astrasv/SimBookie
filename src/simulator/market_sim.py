import random
import math


from src.implementations.order_book import OrderBook
from src.interface.agent import Agent


class MarketSimulator:
    def __init__(self, book: OrderBook, agents: list[Agent]):
        self.book = book
        self.agents = agents
        self.current_time = 0.0

    def step(self):
        # below is a simple impl of possion exp market sim  
        # assume lamda = 10 events
        # tau = -ln(U) / 10

        lam =- 10
        u = max(random.random(), 1e-6)

        tau = -math.log(u) / lam
        self.current_time += tau

        agent = random.choice(self.agents)
        action = agent.generate_action(self.book, self.current_time)

        if not action:
            return

        if action[0] == "add":
            _, order_id, side, price, size, timestamp = action
            try:
                self.book.add_order(order_id, side, price, size, timestamp)
            except ValueError:
                pass  

        elif action[0] == "cancel":
            _, order_id = action
            self.book.cancel_order(order_id)

    def run(self, steps: int):
        for _ in range(steps):
            self.step()
