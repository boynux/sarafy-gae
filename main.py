# -*- coding: utf-8 -*-
import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), "lib"))

import webapp2
import gaemechanize
import re

from bs4 import BeautifulSoup
from abc import ABCMeta
from abc import abstractmethod

from extractor import Crawler, ExtractorImpl, Extractor, ExtractorResult, SarafikishImpl
import httpclient

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
        


class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Hello, World!')

class HealthCheck(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'application/json'
        self.response.write('{"status": "running"}')

class ExchangeRates(webapp2.RequestHandler):
    def get(self):
        extractor = Extractor(SarafikishImpl((httpclient.Client())))
        result = extractor.get_result().get_json()
        
        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(result)

application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/health', HealthCheck),
    ('/exchange-rates', ExchangeRates),
], debug=True)

