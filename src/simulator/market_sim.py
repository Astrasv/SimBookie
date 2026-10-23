import random
import math
import time


from src.implementations.order_book import OrderBook
from src.interface.agent import Agent


class MarketSimulator:
    def __init__(self, book: OrderBook, agents: list[Agent]):
        self.book = book
        self.agents = agents
        self.current_time = time.time()

    def step(self):
        # below is a simple impl of possion exp market sim  
        # assume lamda = 10 events
        # tau = -ln(U) / 10

        lam = 10
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
                print(f"Order ({order_id}, {side}, {price}, {size}, {timestamp})")
            except ValueError:
                pass  

        elif action[0] == "cancel":
            _, order_id = action
            self.book.cancel_order(order_id)
            print(f"Cancelled ({order_id})")
            
        elif action[0] == "market":
            _, side, size  = action
            self.book.execute_market_order(side, size)
            print(f"Executed Market Order ({side},{size})")
            

    def run(self, steps: int):
        for _ in range(steps):
            self.step()
