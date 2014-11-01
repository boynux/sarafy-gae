import httplib, urllib2, urllib
from urlparse import urlparse

class Client:
    headers = {}

    def setHeader(self, name, value):
        self.headers[name] = value
        return self.headers[name]

    def get(self, url, query = {}):
        if query:
            queryString = urllib.urlencode(query) 
            url += "%s%s" % ('&' if '?' in url else '?', queryString)

        request = urllib2.Request(url, None, self.headers)
        request.get_method = lambda: 'GET'

        handle = self._connect(request)
        return Response(handle)

    def __updateQuery(self, newQuery):
        self.query = reduce(lambda x,y: dict(x.items() + y.items()), [query, newQuery])

    def _connect(self, request):
        return urllib2.urlopen(request)

class Response:
    def __init__(self, response):
        self.response = response
        self.body = None

    def getBody(self):
        if self.body is None:
            self.body = self.response.read()
            self.response.close()

        return self.body
        
class UserAgent:
    Firefox = 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.3) Gecko/20100423 Ubuntu/10.04 (lucid) Firefox/3.6.3'

if __name__ == "__main__":
    client = Client()
    client.setHeader('User-Agent', UserAgent.Firefox)
    response = client.get('http://ifconfig.me/all')
    print response.getBody()
