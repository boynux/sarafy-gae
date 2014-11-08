from abc import ABCMeta, abstractmethod

class Aggregator:
  aggregators = []

  __metaclass__ = ABCMeta

  def __call__(self, data):
    for agg in self.aggregators:
      data = agg(data)

    return self.map(data)

  @abstractmethod
  def map(self, data):
    pass

  def add(self, aggregator):
    if aggregator is not Aggregator:
      raise TypeError()

    self.aggregators.add(aggregator)

class Average(Aggregator):
  def map(self, data):
    return reduce(lambda x, y: x + y, data)/len(data)


