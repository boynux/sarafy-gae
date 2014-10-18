# -*- coding: utf-8 -*-

import webapp2
import gaemechanize
import re

from bs4 import BeautifulSoup
from abc import ABCMeta
from abc import abstractmethod

class Crawler:
    def __init__(self, url = None):
        self.url = url
        self.is_open = False

    def open(self, url = ''):
        if not self.is_open:
            self.br = gaemechanize.Browser()
            self.br.set_handle_refresh(False)
            self.set_useragent()

            self.response = self.br.open(self.url or url)
            self.is_open = True

    def set_useragent(self):
        if self.br:
            self.br.addheaders = [
                ('User-Agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.3) Gecko/20100423 Ubuntu/10.04 (lucid) Firefox/3.6.3'),
                ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
            ]
    def get_current_title(self):
        if self.br:
            return self.br.title()

    def get_html(self):
        return self.response.read()

class Extractor:
    def set_strategy(self, strategy):
        self.strategy = strategy

    def get_result(self):
        return ExtractorResult(self.strategy.get_data())

class ExtractorImpl:
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_data(self):
        pass

class MesghaalImpl(ExtractorImpl):
    weburl = "http://www.mesghaal.com/";

    def __init__(self, crawler):
        self.crawler = crawler

    def get_data(self):
        bs  = BeautifulSoup(self.__read())
        rows = bs.find(class_="MsoTableLightGridAccent6").find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            for col in cols:
                text = col.get_text().encode('utf8', 'replace')
                if text == 'US dollar':
                    print text
        
    def __open(self):
        self.crawler.open(self.weburl)

    def __read(self):
        self.__open()
        return self.crawler.get_html()

class MazanneImpl(ExtractorImpl):
    def __init__(self, crawler):
        self.crawler = crawler

    def get_data(self):
        bs  = BeautifulSoup(self.__read())
        rows = bs.find(id="hor-minimalist-b").find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            if len(cols) == 2 and cols[0] == u'دلار آمریکا':
                print cols[1]
        
    def __open(self):
        self.crawler.open('http://www.mazanne.com/')

    def __read(self):
        self.__open()
        return self.crawler.get_html()
        
class ExtractorResult:
    def __init__(self, result):
        self.result = result

    def get_json(self):
        return '{"title": "%s"}' % self.result

class ExtractorStrategy:
    pass


class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Hello, World!')

class ExchangeRates(webapp2.RequestHandler):
    def get(self):
        extractor = Extractor()
        extractor.set_strategy(MesghaalImpl(Crawler()))
        result = extractor.get_result().get_json()
        
        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(result)

application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/exchange-rates', ExchangeRates),
], debug=True)

