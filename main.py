# -*- coding: utf-8 -*-
import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), "lib"))

import webapp2
import re

from bs4 import BeautifulSoup
from abc import ABCMeta
from abc import abstractmethod

from exchangerate import ExchangeRate
from aggregators import Average
from extractor import Crawler, ExtractorImpl, Extractor, ExtractorResult, SarafikishImpl, MazanexImpl, ArzliveImpl
import httpclient

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

class ExchangeRatesAverage(webapp2.RequestHandler):
    def get(self):
        exchangeRate = ExchangeRate(to = ['USD', 'EUR', 'GBP', 'MYR'])
        exchangeRate.addAggregator(Average())

        exchangeRate.addExtractor(Extractor(SarafikishImpl((httpclient.Client()))))
        exchangeRate.addExtractor(Extractor(MazanexImpl((httpclient.Client()))))
        exchangeRate.addExtractor(Extractor(ArzliveImpl((httpclient.Client()))))

        result = exchangeRate.getResult().get_json()

        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(result)

application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/health', HealthCheck),
    ('/exchange-rates', ExchangeRates),
    ('/exchange-rates/average', ExchangeRatesAverage),
], debug=True)

