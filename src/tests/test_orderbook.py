import unittest
from src.implementations.order_book import OrderBook
from src.models.order import Order


class TestOrderBook(unittest.TestCase):

    def setUp(self):
        self.book = OrderBook()

    def test_empty_book(self):
        self.assertIsNone(self.book.get_best_bid())
        self.assertIsNone(self.book.get_best_ask())

    def test_add_single_orders(self):
        self.book.add_order(1, 'buy', 100.0, 10.0, 1.0)
        self.book.add_order(2, 'sell', 101.0, 20.0, 2.0)

        self.assertEqual(self.book.get_best_bid(), (100.0, 10.0))
        self.assertEqual(self.book.get_best_ask(), (101.0, 20.0))

    def test_price_priority_bids(self):
        self.book.add_order(1, 'buy', 99.0, 10.0, 1.0)
        self.book.add_order(2, 'buy', 100.0, 15.0, 2.0)

        self.assertEqual(self.book.get_best_bid(), (100.0, 15.0))

    def test_price_priority_asks(self):
        self.book.add_order(1, 'sell', 102.0, 10.0, 1.0)
        self.book.add_order(2, 'sell', 101.0, 5.0, 2.0)

        self.assertEqual(self.book.get_best_ask(), (101.0, 5.0))

    def test_time_priority_same_price(self):
        self.book.add_order(1, 'buy', 100.0, 10.0, 1.0)
        self.book.add_order(2, 'buy', 100.0, 20.0, 2.0)

        level = self.book.bid_levels[100.0]


        self.assertEqual(level.head.order_id, 1)
        self.assertEqual(level.tail.order_id, 2)


        self.assertEqual(level.total_size, 30.0)

    def test_cancel_order(self):
        self.book.add_order(1, 'buy', 100.0, 10.0, 1.0)
        self.book.add_order(2, 'buy', 100.0, 20.0, 2.0)

        cancelled = self.book.cancel_order(1)
        self.assertIsNotNone(cancelled)
        self.assertEqual(cancelled.order_id, 1)

        self.assertEqual(self.book.get_best_bid(), (100.0, 20.0))

    def test_price_level_cleanup_on_cancel(self):
        self.book.add_order(1, 'buy', 100.0, 10.0, 1.0)
        self.book.cancel_order(1)

        self.assertNotIn(100.0, self.book.bid_levels)
        self.assertNotIn(-100.0, self.book.bid_prices)
        self.assertIsNone(self.book.get_best_bid())

    def test_duplicate_order_id_raises_error(self):
        self.book.add_order(1, 'buy', 100.0, 10.0, 1.0)
        with self.assertRaises(ValueError):
            self.book.add_order(1, 'buy', 101.0, 5.0, 2.0)

    def test_cancel_nonexistent_order(self):
        result = self.book.cancel_order(999)
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()