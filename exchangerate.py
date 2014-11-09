from extractor import ExtractorResult

class ExchangeRate():
  aggregator = None

  def __init__(self, fr = 'IRR', to = 'USD'):
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
    if self.aggregator:
      return [{
        self.fr: {
          self.to: {
            'BID': self.aggregator([x[self.fr][self.to]['BID'] for x in data]),
            'ASK': self.aggregator([x[self.fr][self.to]['ASK'] for x in data]),
            }
          }
        }]

    return [{
      self.fr: {
          self.to: {
            'BID': [x[self.fr][self.to]['BID'] for x in data],
            'ASK': [x[self.fr][self.to]['ASK'] for x in data]
            }
         }
      }]

