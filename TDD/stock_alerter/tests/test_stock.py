import unittest

"""
try: 
    from context import stock_alerter
except Exception as e:
    print(e)
    from .context import stock_alerter
"""

from stock_alerter.stock import Stock


class StockTest(unittest.TestCase):
    def test_price_of_a_new_stock_class_should_be_none(self):
        stock = Stock("GOOG")
        self.assertIsNone(stock.price)

    def test_price_of_another_stock_should_be_none(self):
        stock = Stock("AAPL")
        self.assertIsNone(stock.price)


if __name__ == "__main__":
    unittest.main()
