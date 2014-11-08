import os
import unittest
import mock
import extractor
import html5lib
import xml.etree.ElementTree as ET
import json

from extractor import Crawler, Extractor, MesghaalImpl, SarafikishImpl

class TesExtractor(unittest.TestCase):
    def test_crawlerInitialize(self):
        crawler = Crawler()
        self.assertIsInstance(crawler, Crawler)

    @mock.patch('extractor.Client')
    def test_CrawlerOpenUrl(self, client):
        crawler = Crawler()
        crawler.open("http://ifconfig.me/ip")

        client().get.assert_called_once_with("http://ifconfig.me/ip")

    @mock.patch('extractor.Client')
    def test_crawlerGetBody(self, client):
        client().get().getBody.return_value = '<html>'

        crawler = Crawler()
        crawler.open("http://ifconfig.me/ip")
        result = crawler.get_html()
        
        client().get().getBody.assert_called_once_with()

    def test_extractorGetResult(self):
        strategy = mock.MagicMock()
        crawler = mock.MagicMock()
        extractor = Extractor(strategy)
        extractor.get_result()

        strategy.get_data.assert_called_once_with()

    def test_MesghaalImpInstance(self):
        dom = html5lib.parse('<html><head></head><body><p>Hi</p></body></html>', namespaceHTMLElements=False);
        with mock.patch('httpclient.Client') as client:
            impl = MesghaalImpl(client)

    def test_SarafikishImpInstance(self):
        json = "{}"
        with mock.patch('httpclient.Client') as client:
            impl = SarafikishImpl(client)

    def test_SarafikishImpUSDParser(self):
        with open(os.path.join(os.path.dirname(__file__), 'fixtures/sarafikish-01.html')) as f:
            with mock.patch('httpclient.Client') as client:
                client.get().getBody.return_value = f.read()              
                impl = SarafikishImpl(client)
                result = impl.get_data()

                self.assertIsNotNone(result, "get data result is None!")
                self.assertTrue('IRR' in result, "Can not find IRR commodity in result")
                self.assertTrue(
                    all(map(lambda i: i in result['IRR'], ['USD', 'EUR', 'AED'])),
                    "Can not find XXX => IRR commodity in result: " + result["IRR"].__repr__()
                )

    def test_SarafikishImpGoldParser(self):
        with open(os.path.join(os.path.dirname(__file__), 'fixtures/sarafikish-01.html')) as f:
            with mock.patch('httpclient.Client') as client:
                client.get().getBody.return_value = f.read()              
                impl = SarafikishImpl(client)
                result = impl.get_data()

                self.assertIsNotNone(result, "get data result is None!")
                self.assertTrue('IRR' in result, "Can not find IRR gold commodity in result")
                self.assertTrue(
                    all(map(lambda i: i in result['IRR'], ['24K'])),
                    "Can not find GOLD => IRR commodity in result: " + result["IRR"].__repr__()
                )

                print result
