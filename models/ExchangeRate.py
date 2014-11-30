from google.appengine.ext import ndb as db

class ExchangeRate(db.Model):
  fr = db.StringProperty(required=True)
  to = db.StringProperty(required=True)
  bid = db.FloatProperty(required=True)
  ask = db.FloatProperty(required=True)
  date = db.DateTimeProperty(auto_now_add=True)

  def query_rates(cls, ancestor_key):
    return cls.query(ancestor=ancestor_key).order(-cls.date)

