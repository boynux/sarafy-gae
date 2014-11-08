import unittest, mock, os
from exchangerate import ExchangeRate
from extractor import Extractor, SarafikishImpl, MazanexImpl
from aggregators import Average
from httpclient import Client

class TestExchangeRate(unittest.TestCase):
  def test_ExchangeRateInstantiation(self):
    exchangeRate = ExchangeRate()
    self.assertIsInstance(exchangeRate, ExchangeRate)

  def test_ExchangeRateWithOneExtractor(self):
    exchangeRate = ExchangeRate()
    with open(os.path.join(os.path.dirname(__file__), 'fixtures/sarafikish-01.html')) as f:
        with mock.patch('httpclient.Client') as client:
            client.get().getBody.return_value = f.read()
            extractor = Extractor(SarafikishImpl((client)))

            exchangeRate.addExtractor(extractor)
            result = exchangeRate.getResult().get_data()

            self.assertTrue(len(result) == 1)
            self.assertTrue("IRR" in result[0])

  def test_ExchangeRateFromMultilpleExtractors(self):
    exchangeRate = ExchangeRate()
    with open(os.path.join(os.path.dirname(__file__), 'fixtures/sarafikish-01.html')) as f:
        with mock.patch('httpclient.Client') as client:
            client.get().getBody.return_value = f.read()
            exchangeRate.addExtractor(Extractor(SarafikishImpl((client))))

    with open(os.path.join(os.path.dirname(__file__), 'fixtures/mazanex-01.html')) as f:
        with mock.patch('httpclient.Client') as client:
            client.get().getBody.return_value = f.read()
            exchangeRate.addExtractor(Extractor(MazanexImpl((client))))

    result = exchangeRate.getResult().get_data()

    self.assertTrue(len(result) == 1)
    self.assertTrue(len(result[0]) == 2)
    self.assertTrue("IRR" in result[0])

  def test_ExchangeRateFromMultilpleExtractors(self):
    exchangeRate = ExchangeRate()
    with open(os.path.join(os.path.dirname(__file__), 'fixtures/sarafikish-01.html')) as f:
        with mock.patch('httpclient.Client') as client:
            client.get().getBody.return_value = f.read()
            exchangeRate.addExtractor(Extractor(SarafikishImpl((client))))

    with open(os.path.join(os.path.dirname(__file__), 'fixtures/mazanex-01.html')) as f:
        with mock.patch('httpclient.Client') as client:
            client.get().getBody.return_value = f.read()
            exchangeRate.addExtractor(Extractor(MazanexImpl((client))))

    result = exchangeRate.getResult().get_data()

    self.assertTrue(len(result) == 1)
    self.assertTrue(len(result[0]) == 1)
    self.assertTrue("IRR" in result[0])

  def test_ExchangeRateWithAgerageAggregator(self):
    exchangeRate = ExchangeRate()
    exchangeRate.addAggregator(Average())

    with open(os.path.join(os.path.dirname(__file__), 'fixtures/sarafikish-01.html')) as f:
        with mock.patch('httpclient.Client') as client:
            client.get().getBody.return_value = f.read()
            exchangeRate.addExtractor(Extractor(SarafikishImpl((client))))

    with open(os.path.join(os.path.dirname(__file__), 'fixtures/mazanex-01.html')) as f:
        with mock.patch('httpclient.Client') as client:
            client.get().getBody.return_value = f.read()
            exchangeRate.addExtractor(Extractor(MazanexImpl((client))))

    result = exchangeRate.getResult().get_data()
    self.assertTrue(len(result) == 1, 'There should be only one item in the list')
    self.assertTrue("IRR" in result[0])

