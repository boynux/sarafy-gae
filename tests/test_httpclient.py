#!env python

import unittest
import mock
import httpclient, urllib2

class TestHttpClient(unittest.TestCase):
    def setUp(self):
        self.client = httpclient.Client()

    def test_setUserAgent(self):
        agent = self.client.setHeader('User-Agent', httpclient.UserAgent.Firefox)
        self.assertEqual(agent, 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.3) Gecko/20100423 Ubuntu/10.04 (lucid) Firefox/3.6.3')


    def test_fetchUrl(self):
        url = 'http://www.google.com/about'
        opener, mockResponse = self._installMockUrllibOpener()

        response = self.client.get(url)

        self.assertTrue(opener.open.called, "Url opener not called!")
        self.assertEqual(1, len(opener.open.call_args_list), "Seems Url open request triggered more than once")

        args, kwargs = opener.open.call_args
        request = args[0]

        self.assertEqual(url, request.get_full_url(), "Request url does not match with the actual.")

    def test_responseObject(self):
        url = 'http://ifconfig.me/ip'
        opener, mockResponse = self._installMockUrllibOpener()

        response = self.client.get(url)
        self.assertIsInstance(response, httpclient.Response, "Response is not valid!")

    def test_responseContainsBody(self):
        url = 'http://ifconfig.me/ip'
        opener, mockResponse = self._installMockUrllibOpener(body = "127.0.0.1")

        body = self.client.get(url).getBody()
        self.assertEqual("127.0.0.1", body)

        mockResponse.read.assert_called_with()

    def test_requsetQueryString(self):
        url = 'http://ifconfig.me/ip'
        opener, mockResponse = self._installMockUrllibOpener(body = "127.0.0.1")

        body = self.client.get(url, {'q': 1})
        args, kwargs = opener.open.call_args
        request = args[0]

        self.assertEqual(url + '?q=1', request.get_full_url(), "Request url does not match with the actual.")

    def test_SetUserAgent(self):
        agent = self.client.setHeader('User-Agent', httpclient.UserAgent.Firefox)
        url = 'http://ifconfig.me/ip'

        opener, _ = self._installMockUrllibOpener(body = "127.0.0.1")

        registeredAgent = self.client.setHeader("User-Agent", agent)
        self.assertEqual(agent, registeredAgent)

    def test_requestHasCorrectUserAgent(self):
        agent = self.client.setHeader('User-Agent', httpclient.UserAgent.Firefox)
        url = 'http://ifconfig.me/ip'

        opener, _ = self._installMockUrllibOpener(body = "127.0.0.1")
        self.client.setHeader('User-Agent', agent)

        body = self.client.get(url).getBody()
        args, kwargs = opener.open.call_args

        headers = args[0].header_items()
        self.assertTrue(('User-agent', agent) in headers)

    def _installMockUrllibOpener(self, body = "OK"):
        opener = mock.MagicMock()
        response = mock.MagicMock()
        response.read.return_value = body

        opener.open = mock.MagicMock(return_value = response)

        urllib2.install_opener(opener)
        return opener, response


def Any(cls):
    class Any(cls):
        def __eq__(self, other):
            return True

    return Any()
