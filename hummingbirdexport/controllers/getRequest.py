import requests
import json
import hummingbirdexport.config as config

# TODO: This probably shouldn't even be a class.
class getRequest(object):
    def getInfo(self, username):
        # Authenticate Hummingbird API client
        url = 'https://hummingbirdv1.p.mashape.com/users/authenticate'
        headers = { "X-Mashape-Authorization": config.humming_mashape }
        response = requests.post(url, headers=headers, data=config.humming_auth)
        auth_token = response.text.encode('utf8')[1:-1]

        # Fetch user library page.
        url = "https://hummingbirdv1.p.mashape.com/users/{}/library".format(username)
        response = requests.get(url, params=dict(auth_token=auth_token), headers=headers)

        return json.loads(response.text.encode('utf8'))
