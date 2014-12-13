# -*- coding: utf-8 -*-
import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), "lib"))

import webapp2, re, json
import httpclient
import datetime
from time import mktime

from bs4 import BeautifulSoup
from abc import ABCMeta
from abc import abstractmethod

from google.appengine.ext import ndb
from exchangerate import ExchangeRate
from aggregators import Average
from extractor import Crawler, ExtractorImpl, Extractor, ExtractorResult, SarafikishImpl, MazanexImpl, ArzliveImpl
from handlers import FlagsHandler
from models.ExchangeRate import ExchangeRate as ER

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
        to = ['USD', 'EUR', 'GBP', 'MYR']
        result = ER.query_last_changes('Sarafikish', 'IRR', to)

        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(json.dumps(result, cls = JsonEncoder))

class ExchangeRatesAverage(webapp2.RequestHandler):
    def get(self):
        to = ['USD', 'EUR', 'GBP', 'MYR']
        flagsHandler = FlagsHandler("%s/cdn/images" % self.request.host_url)
        result = flagsHandler(ER.query_last_changes('Average', 'IRR', to))

        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(json.dumps(result, cls = JsonEncoder))

class JsonEncoder(json.JSONEncoder):
  def default(self, obj):
    if isinstance(obj, datetime.datetime):
      return obj.strftime('%Y-%m-%d %H:%I:%S')

    return json.JSONEncoder.default(self, obj)

application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/health', HealthCheck),
    ('/exchange-rates', ExchangeRates),
    ('/exchange-rates/average', ExchangeRatesAverage),
], debug=True)

