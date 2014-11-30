import string

from google.appengine.ext import ndb as db

class ExchangeRate(db.Model):
  fr = db.StringProperty(required=True)
  to = db.StringProperty(required=True)
  bid = db.FloatProperty(required=True)
  ask = db.FloatProperty(required=True)
  date = db.DateTimeProperty(auto_now_add=True)

  @classmethod
  def query_rates(cls, ancestor_key, fr):
    query = cls.query(cls.fr == fr, ancestor = ancestor_key).order(-cls.date)

    rates = {}
    for rate in query:
      yield rate

  @classmethod
  def query_last_changes(cls, strategy, fr, to):
    rates = cls.query_rates(db.Key('ExchangeRate', string.capwords(strategy)), fr)

    result = {}

    for rate in rates:
      if rate.to not in result.keys():
        result[rate.to] = {
          'BID': rate.bid,
          'ASK': rate.ask,
          'LastUpdate': rate.date.strftime('%Y-%m-%d %H:%I:%S')
        }

      elif 'Changes' not in result[rate.to]:
        result[rate.to]['Changes'] = (result[rate.to]['ASK'] - rate.ask) / rate.ask if rate.ask != 0 and result[rate.to]['ASK'] != 0 else 0.0

      if set(result.keys()) == set(to) and all('Changes' in x for x in result.values()):
        break

    return result

