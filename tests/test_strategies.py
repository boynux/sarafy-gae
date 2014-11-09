import os, unittest, mock, html5lib

from extractor import Crawler, Extractor, ExtractorImpl, MesghaalImpl, SarafikishImpl, MazanexImpl, ArzliveImpl

class StertegiesImplTest(unittest.TestCase):
    def test_MesghaalImpInstance(self):
        dom = html5lib.parse('<html><head></head><body><p>Hi</p></body></html>', namespaceHTMLElements=False);
        with mock.patch('httpclient.Client') as client:
            impl = MesghaalImpl(client)

    def test_SarafikishImpInstance(self):
        with mock.patch('httpclient.Client') as client:
            impl = SarafikishImpl(client)

            self.assertIsInstance(impl, SarafikishImpl)
            self.assertIsInstance(impl, ExtractorImpl)

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

                self.assertEqual(32376.0, result["IRR"]["USD"]["BID"])
                self.assertEqual(32907.0, result["IRR"]["USD"]["ASK"])

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
                self.assertEqual(1212215.0, result["IRR"]["24K"])

    def test_MazanexImplInstance(self):
        with mock.patch('httpclient.Client') as client:
            impl = MazanexImpl(client)

            self.assertIsInstance(impl, MazanexImpl)
            self.assertIsInstance(impl, ExtractorImpl)

    def test_MazanexImplParser(self):
        with open(os.path.join(os.path.dirname(__file__), 'fixtures/mazanex-01.html')) as f:
            with mock.patch('httpclient.Client') as client:
                client.get().getBody.return_value = f.read()
                impl = MazanexImpl(client)
                result = impl.get_data()

                self.assertIsNotNone(result, "get data result is None!")
                self.assertTrue('IRR' in result, "Can not find IRR commodity in result")
                self.assertTrue(
                    all(map(lambda i: i in result['IRR'], ['USD', 'GBP', 'MYR'])),
                    "Can not find XXX => IRR commodity in result: " + result["IRR"].__repr__()
                )

                self.assertEqual(0.0, result["IRR"]["USD"]["BID"])
                self.assertEqual(32480.0, result["IRR"]["USD"]["ASK"])

                self.assertEqual(0.0, result["IRR"]["GBP"]["BID"])
                self.assertEqual(51547.373432788445, result["IRR"]["GBP"]["ASK"])

                self.assertEqual(0.0, result["IRR"]["MYR"]["BID"])
                self.assertEqual( 9709.434413487981, result["IRR"]["MYR"]["ASK"])

    def test_ArzliveImplInstance(self):
        with mock.patch('httpclient.Client') as client:
            impl = ArzliveImpl(client)

            self.assertIsInstance(impl, ArzliveImpl)
            self.assertIsInstance(impl, ExtractorImpl)

    def test_ArzliveImplUSDParser(self):
        with open(os.path.join(os.path.dirname(__file__), 'fixtures/arzlive-01.html')) as f:
            with mock.patch('httpclient.Client') as client:
                client.get().getBody.return_value = f.read()
                impl = ArzliveImpl(client)
                result = impl.get_data()

                self.assertIsNotNone(result, "get data result is None!")
                self.assertTrue('IRR' in result, "Can not find IRR commodity in result")
                self.assertTrue(
                    all(map(lambda i: i in result['IRR'], ['USD', 'MYR', 'GBP'])),
                    "Can not find XXX => IRR commodity in result: " + result["IRR"].__repr__()
                )
                self.assertEqual(0.0, result["IRR"]["USD"]["BID"])
                self.assertEqual(32480.0, result["IRR"]["USD"]["ASK"])

                self.assertEqual(0.0, result["IRR"]["MYR"]["BID"])
                self.assertEqual(9638.0, result["IRR"]["MYR"]["ASK"])

                self.assertEqual(0.0, result["IRR"]["GBP"]["BID"])
                self.assertEqual(51156.0, result["IRR"]["GBP"]["ASK"])

