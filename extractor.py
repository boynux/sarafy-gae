import html5lib, json, locale
import xml.etree.ElementTree as ET

from bs4 import BeautifulSoup
from abc import ABCMeta, abstractmethod
from httpclient import Client,UserAgent

class Crawler:
    def __init__(self, url = None):
        self.url = url
        self.is_open = False

    def open(self, url = None):
        if not self.is_open:
            client = Client()
            client.setHeader('User-Agent', UserAgent.Firefox)

            self.response = client.get(url)
            self.is_open = True

        return self.is_open

    def get_html(self):
        if self.is_open:
            return html5lib.parse(self.response.getBody(), encoding='UTF-8', namespaceHTMLElements=False);

        raise Exception("HTTP call is not initiated. First call open() please.")

class Extractor:
    def __init__(self, strategy):
        self.strategy = strategy

    def set_strategy(self, strategy):
        self.strategy = strategy

    def get_result(self):
        return ExtractorResult(self.strategy.get_data())

class ExtractorResult:
    def __init__(self, result):
        self.result = result

    def get_data(self):
        return self.result

    def get_json(self):
        return json.dumps(self.result)

    def format(self):
        pass

class ExtractorImpl:
    __metaclass__ = ABCMeta

    def __init__(self, client):
        self.client = client

    def get_data(self):
        return self._get_data(self._fetch_data())

    @abstractmethod
    def _fetch_data(self):
        pass

    @abstractmethod
    def _get_data(self, data):
        pass

class SarafikishImpl(ExtractorImpl):
    weburl = "http://quote2.sarafikish.com/?task=bid"
    headers = {'referer': 'http://www.sarafikish.com/Havaalejat/nerkhe-arz-1.html'}

    def _fetch_data(self):
        for key in self.headers:
            self.client.setHeader(key, self.headers[key])

        jsonp = self.client.get(self.weburl).getBody()
        return jsonp[8:-2]

    def _get_data(self, data):
        return self.__processJson(data)

    def __processJson(self, jsonString):
        result = {"IRR": {}}

        for commodity, values in json.loads(jsonString).iteritems():
            if commodity in ["USDIRT", "EURIRT", "AEDIRT"]:
                result["IRR"][str(commodity[0:3])] = {
                    "ASK": values["ask"] * 10000,
                    "BID": values["bid"] * 10000
                }

            if commodity in ["GOLD24"]:
                result["IRR"][str(commodity[-2:] + "K")] = values["ask"] * 10000
        return result

class MazanexImpl(ExtractorImpl):
    weburl = "http://www.mazanex.com"

    def _fetch_data(self):
        html = self.client.get(self.weburl).getBody()
        return html

    def _get_data(self, data):
        dom = html5lib.parse(data, namespaceHTMLElements=False)
        return self.__processHtml(dom)

    def __processHtml(self, dom):
        cols = dom.findall(".//table[@id='m_tbl']//tr[2]/td")
        usdAsk = float(str(cols[1].text).translate(None, ','))
        usdBid = 0.0 if cols[2].text == u'-' else float(str(cols[2].text).translate(None, ','))

        return {'IRR': {'USD': { 
            'ASK': usdAsk * 1.0,
            'BID': usdBid * 1.0
            }
        }}

# Mesghaal implementation. (this service is absolette
class MesghaalImpl(ExtractorImpl):
    weburl = "http://www.mesghaal.com/";

    def _fetch_data(self):
        pass

    def _get_data(self, data):
        return self.__processHtml(data)

    def __processHtml(self, dom):
        rows = dom.iter('tr')
        for row in rows:
            for col in row.iter('td'):
                token = ""
                for text in col.itertext():
                    token += text.encode('utf-8').strip() if text else ""

                print token
#
