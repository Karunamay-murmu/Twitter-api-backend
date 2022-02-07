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
    def user_followers(self, path, id):
        endpoint = "/users/{}/{}".format(id, path)
        url = self.BASE_URL + endpoint
        return url

    @classmethod
    def user_following(self, id):
        endpoint = "/users/{}/following".format(id)
        url = self.BASE_URL + endpoint
        return url

    @classmethod
    def user_timeline(self, id):
        endpoint = "/users/{}/tweets".format(id)
        return self.BASE_URL + endpoint

    @classmethod
    def user_liked_tweets(self, id):
        return self.BASE_URL + "/users/{}/liked_tweets".format(id)

    @classmethod
    def tweets_lookup(self, ids):
        param = ",".join(str(id) for id in ids)
        endpoint = "/tweets?ids={}".format(param)
        return self.BASE_URL + endpoint

    @classmethod
    def tweet_lookup(self, id):
        return self.BASE_URL + "/tweets/{}".format(id)
        
    @classmethod
    def get_user_mentions_by_id(self, id):
        endpoint = "/users/{}/mentions".format(id)
        url = self.BASE_URL + endpoint
        return url

    @classmethod
    def tweet_search(self):
        endpoint = "/tweets/search/recent"
        return self.BASE_URL + endpoint


    # v1 endpoints
    @classmethod
    def search_users(self):
        return self.BASE_URL_V1 + USERS_SEARCH

    @classmethod
    def show_user(self):
        return self.BASE_URL_V1 + USERS_SHOW

    @classmethod
    def users_timeline(self):
        return self.BASE_URL_V1 + USERS_TIMELINE

    @classmethod
    def users_home_timeline(self):
        return self.BASE_URL_V1 + "/statuses/home_timeline.json"
