from google.appengine.ext import ndb as db

class ExchangeRate(db.Model):
  fr = db.StringProperty(required=True)
  to = db.StringProperty(required=True)
  bid = db.FloatProperty(required=True)
  ask = db.FloatProperty(required=True)
  date = db.DateTimeProperty(auto_now_add=True)

  @classmethod
  def query_rates(cls, ancestor_key, fr, to):
    query = cls.query(cls.fr == fr, ancestor = ancestor_key)
    query.order(-cls.date)

    rates = {}
    for rate in query:
        if rate.fr not in rates.keys():
            rates[rate.to] = {
                'ASK': rate.ask,
                'BID': rate.bid,
                'LastUpdate': rate.date.strftime("%d-%m-%Y %H:%I:%S")
            }

        if set(to) == set(rates.keys()):
            break

    return rates

