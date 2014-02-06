import urllib
import urllib2
import json

class getRequest(object):

    def __init__(self):
        pass
    
    def getInfo(self, uname):
        """
        The Hummingbird api requires a valid user and password for authentication before
        returning any data. For ease of use I have created an account to do this, rather than
        have a user input their personal username and password. apiuname and passw have been
        intentionally left blank in the public source
        """
        apiuname = ""
        passw = ""
        url = 'https://hummingbirdv1.p.mashape.com/users/authenticate'
        values = {'username' : apiuname,
                  'password' : passw }

        """
        Mashape requires an account to access their api, for more information of Mashape and
        the Hummingbird API, visit https://www.mashape.com/vikhyat/hummingbird-v1
        My API key has been intentionally left blank in the public source.
        """     
        headers = { "X-Mashape-Authorization": "" }

        data = urllib.urlencode(values)
        req = urllib2.Request(url, data, headers)
        response = urllib2.urlopen(req)
        authToken = response.read()
        authToken = authToken[1:-1]

        request = urllib2.Request("https://hummingbirdv1.p.mashape.com/users/" + uname + "/library?auth_token=" + authToken)
        
        """
        Mashape requires an account to access their api, for more information of Mashape and
        the Hummingbird API, visit https://www.mashape.com/vikhyat/hummingbird-v1
        My API key has been intentionally left blank in the public source.
        """     
        request.add_header("X-Mashape-Authorization", "")
        response = urllib2.urlopen(request)

        return json.loads(response.read())