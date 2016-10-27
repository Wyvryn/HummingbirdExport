import json
import re
import time

import requests

import hummingbirdexport.config as config
import redis


class Hummingbird:

    def __init__(self):
        # Authenticate Hummingbird API client
        url = 'https://hummingbirdv1.p.mashape.com/users/authenticate'
        self.headers = {"X-Mashape-Authorization": config.humming_mashape}
        response = requests.post(url, headers=self.headers, data=config.humming_auth)
        self.auth_token = response.text[1:-1]

    def get_library(self, username):
        """Fetch user library page."""
        url = "https://hummingbirdv1.p.mashape.com/users/{}/library".format(username)
        response = requests.get(url, params=dict(auth_token=self.auth_token), headers=self.headers)

        return json.loads(response.text)


class MyAnimeList:

    def __init__(self):
        # Connect to Redis if Redis caching is enabled.
        if config.redis['enabled']:
            self.redis = redis.StrictRedis(host=config.redis['host'],
                                           port=config.redis['port'],
                                           db=config.redis['db'],
                                           password=config.redis['password'])
        else:
            self.redis = None

    def get_anime_id(self, title):
        """Attempt to find the id of an anime by its title.

        On success str is returned, otherwise None."""

        # Check Redis cache before doing anything.
        if self.redis:
            anime_id = self.redis.get(title)
            if anime_id:
                return anime_id.decode('utf8')

        # Actually perform the API request on cache miss.
        # TODO: Make sure we aren't waiting too much.
        time.sleep(2.5)
        url = "http://myanimelist.net/api/anime/search.xml"
        response = requests.get(url, params=dict(q=title.strip()), auth=config.mal_auth)

        match = re.search(r"<id>(.*)</id>", response.text)
        if match:
            anime_id = match.group(1)
            if self.redis:
                self.redis.set(title, anime_id)
            return anime_id
        else:
            return None
