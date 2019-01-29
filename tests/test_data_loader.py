import unittest
import backtester

class TestBackTester(unittest.TestCase):

    def __init__(self):
        self._cont = None

    def test_load_data(self):
        self._cont = backtester.Controller('data/EUR_USD_H1.csv')
        self._cont.loadData()

    def test_increment_time(self):
        self._cont.incrementTime()
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())