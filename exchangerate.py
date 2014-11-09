from extractor import ExtractorResult

class ExchangeRate():
  aggregator = None

  def __init__(self, fr = 'IRR', to = ['USD', 'EUR']):
    self.fr = fr
    self.to = to
    self.extractors = []

  def addExtractor(self, extractor):
    self.extractors.append(extractor)

  def addAggregator(self, aggregator):
    self.aggregator = aggregator

  def getResult(self):
    results = self._aggregate(self._fetchResult())

    return ExtractorResult(results)

  def _fetchResult(self):
    results = []
    for extractor in self.extractors:
      results.append(extractor.get_result().get_data())

    return results

  def _aggregate(self, data):
      result = {self.fr: {}}
      for to in self.to:
        if self.aggregator:
          result[self.fr][to] = {
           'BID': self.aggregator([x[self.fr][to]['BID'] for x in data if to in x[self.fr]]),
           'ASK': self.aggregator([x[self.fr][to]['ASK'] for x in data if to in x[self.fr]]),
          }
        else:
          result[self.fr][to] = {
            'BID': [x[self.fr][to]['BID'] for x in data if to in x[self.fr]],
            'ASK': [x[self.fr][to]['ASK'] for x in data if to in x[self.fr]],
          }


      return [result]
