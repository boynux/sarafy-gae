import string

from google.appengine.ext import ndb as db

class ExchangeRate(db.Model):
  fr = db.StringProperty(required=True)
  to = db.StringProperty(required=True)
  bid = db.FloatProperty(required=True)
  ask = db.FloatProperty(required=True)
  date = db.DateTimeProperty(auto_now_add=True)
  flag_url = db.StringProperty(required=False)

  @classmethod
  def query_rates(cls, ancestor_key, fr):
    query = cls.query(cls.fr == fr, ancestor = ancestor_key).order(-cls.date)

    rates = {}
    for rate in query:
      yield rate

  @classmethod
  def query_last_changes(cls, strategy, fr, to):
    rates = cls.query_rates(db.Key('ExchangeRate', string.capwords(strategy)), fr)

    result = []

    for rate in rates:
      if rate.to not in [x['to'] for x in result]:
        result.append(rate.to_dict())

      elif not all(['changes' in x for x in result if x['to'] == rate.to]):
        for item in [x for x in result if x['to'] == rate.to]:
          item['changes'] = (item['ask'] - rate.ask) / rate.ask if rate.ask != 0 and item['ask'] != 0 else 0.0

      if set(to) == [x['to'] for x in result]:
        break;

    return result

