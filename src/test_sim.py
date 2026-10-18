from src.implementations.order_book import OrderBook
from src.agent.zero_intel_agent import ZeroIntelligenceAgent
from src.simulator.market_sim import MarketSimulator
# 1. Initialize Book and Agents


book = OrderBook()
agents = [ZeroIntelligenceAgent(agent_id=i) for i in range(5)]

# 2. Seed the book with initial liquidity so prices are defined
book.add_order(1, 'buy', 99.50, 100, 0.0)
book.add_order(2, 'sell', 100.50, 100, 0.0)

# 3. Create and run simulation
sim = MarketSimulator(book, agents)
sim.run(steps=1000)

# 4. Inspect results
print('--- Simulation Complete ---')
print('Final Best Bid:', book.get_best_bid())
print('Final Best Ask:', book.get_best_ask())
print(f'Total Active Orders in Book: {len(book.orders)}')