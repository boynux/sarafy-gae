class FlagsHandler:
  def __init__(self, baseUri, size = 48):
    self.baseUri = baseUri
    self.size = 48

  FlagsMap = {
      'USD': 'us',
      'MYR': 'my',
      'GBP': 'gb',
      'EUR': '_European Union'
  }

  def __call__(self, data):
    for item in data:
      item['flag_url'] = "%s/flags/%s/%s.png" % (self.baseUri, self.size, self.FlagsMap[item['to']])

    return data
