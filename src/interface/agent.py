from abc import ABC, abstractmethod

from src.implementations.order_book import OrderBook


class Agent(ABC):
    def __init__(self, agent_id: int):
        self.agent_id = agent_id

    @abstractmethod
    def generate_action(self, book: OrderBook, current_time: float):
        raise NotImplementedError
