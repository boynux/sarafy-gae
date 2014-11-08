import os, unittest, mock, html5lib, json
import xml.etree.ElementTree as ET

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
        extractor = Extractor(strategy)
        extractor.get_result()

        strategy.get_data.assert_called_once_with()

    def test_extractorResultGetData(self):
        strategy = mock.MagicMock()
        strategy.get_data.return_value = {"success": True}
        extractor = Extractor(strategy)
        result = extractor.get_result()

        self.assertTrue(result.get_data()["success"])

        
    def test_extractorResultGetJson(self):
        strategy = mock.MagicMock()
        strategy.get_data.return_value = {"success": True}
        extractor = Extractor(strategy)
        result = extractor.get_result()

        self.assertEqual('{"success": true}', result.get_json())
