import unittest, mock

from aggregators import Aggregator, Average

class TestAggregtors(unittest.TestCase):
  def test_averageInstantiate(self):
    agg = Average()

    self.assertIsInstance(agg, Average)
    self.assertIsInstance(agg, Aggregator)

  def test_averageResult(self):
    agg = Average()
    data = [32000.0, 33000.0, 34000.0]

    self.assertEqual(agg(data), 33000.0)
