from django.conf import settings

from request.endpoints_v2 import USERS_SEARCH, USERS_SHOW, USERS_TIMELINE

class Api:

    BASE_URL = settings.TWITTER_API_BASE_URL
    BASE_URL_V1 = settings.TWITTER_API_BASE_URL_V1

    def __init__(self) -> None:
        pass
        
    @classmethod
    def get_user_by_username(self, username):
        endpoint = "/users/by/username/"
        url = self.BASE_URL + endpoint + username
        return url

    @classmethod
    def get_user_tweets_by_id(self, id):
        endpoint = "/users/{}/tweets".format(id)
        url = self.BASE_URL + endpoint
        return url

    @classmethod
    def get_user_mentions_by_id(self, id):
        endpoint = "/users/{}/mentions".format(id)
        url = self.BASE_URL + endpoint
        return url

    @classmethod
    def search_users(self):
        return self.BASE_URL_V1 + USERS_SEARCH

    @classmethod
    def users_show(self):
        return self.BASE_URL_V1 + USERS_SHOW

    @classmethod
    def users_timeline(self):
        return self.BASE_URL_V1 + USERS_TIMELINE
