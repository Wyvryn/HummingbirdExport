import urllib
import urllib2
import json
from keys import api, mashape

class getRequest(object):

    def __init__(self):
        pass
    
    def getInfo(self, uname):
        url = 'https://hummingbirdv1.p.mashape.com/users/authenticate'
        values = {'username' : api['user'],
                  'password' : api['passw']}

        headers = { "X-Mashape-Authorization": mashape }

        data = urllib.urlencode(values)
        req = urllib2.Request(url, data, headers)
        response = urllib2.urlopen(req)
        authToken = response.read()
        authToken = authToken[1:-1]

        request = urllib2.Request("https://hummingbirdv1.p.mashape.com/users/" + uname + "/library?auth_token=" + authToken)
        request.add_header("X-Mashape-Authorization", mashape)
        response = urllib2.urlopen(request)

        return json.loads(response.read())
