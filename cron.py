# -*- coding: utf-8 -*-
import os, sys, string
sys.path.append(os.path.join(os.path.dirname(__file__), "lib"))

import webapp2

from exchangerate import ExchangeRate
from aggregators import Average
from extractor import Crawler, ExtractorImpl, Extractor, ExtractorResult, SarafikishImpl, MazanexImpl, ArzliveImpl
from models.ExchangeRate import ExchangeRate as ExchangeRateModel
from google.appengine.ext import ndb
import httpclient

ExchangeRateTargets = ['USD', 'GBP', 'MYR', 'EUR']

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
        exchangeRate = ExchangeRate(to = ['USD', 'EUR', 'GBP', 'MYR'])
        # exchangeRate.addAggregator(Average())
        exchangeRate.addExtractor(Extractor(SarafikishImpl((httpclient.Client()))))

        result = exchangeRate.getResult().get_json()

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

class DefaultHandler(webapp2.RequestHandler):
  def get(self, strategy):
    cls = string.capwords(strategy) + 'Impl'
    print cls
    exchangeRate = ExchangeRate(to = ExchangeRateTargets)
    exchangeRate.addExtractor(Extractor(globals()[cls]((httpclient.Client()))))

    result = exchangeRate.getResult().get_data()[0]
    print result

    for fr in result:
      for to in result[fr]:
        key = ndb.Key("ExchangeRate", string.capwords(strategy))
        rate = ExchangeRateModel(parent=key, 
            fr = fr,
            to = to,
            ask = result[fr][to]["ASK"][0] if len(result[fr][to]['ASK']) else 0.0,
            bid = result[fr][to]["BID"][0] if len(result[fr][to]['BID']) else 0.0)
        rate.put()

    self.response.headers['Content-Type'] = 'application/json'
    self.response.write(result)

class AverageHandler(webapp2.RequestHandler):
  def get(self):
    exchangeRate = ExchangeRate(to = ExchangeRateTargets)
    exchangeRate.addAggregator(Average())

    exchangeRate.addExtractor(Extractor(SarafikishImpl((httpclient.Client()))))
    exchangeRate.addExtractor(Extractor(MazanexImpl((httpclient.Client()))))
    exchangeRate.addExtractor(Extractor(ArzliveImpl((httpclient.Client()))))

    result = exchangeRate.getResult().get_data()[0]
    print result

    for fr in result:
      for to in result[fr]:
        key = ndb.Key("ExchangeRate", "Average")
        rate = ExchangeRateModel(parent=key, 
            fr = fr,
            to = to,
            ask = result[fr][to]["ASK"],
            bid = result[fr][to]["BID"])
        rate.put()

    self.response.headers['Content-Type'] = 'application/json'
    self.response.write(result)


application = webapp2.WSGIApplication([
    ('/cron/average', AverageHandler),
    ('/cron/(.*)', DefaultHandler)
], debug=True)

