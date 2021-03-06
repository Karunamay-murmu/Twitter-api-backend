from django.conf import settings


class Api:

    BASE_URL = settings.TWITTER_API_BASE_URL
    BASE_URL_V1 = settings.TWITTER_API_BASE_URL_V1

    def __init__(self) -> None:
        pass

    @classmethod
    def user_by_username(cls, username):
        endpoint = "/users/by/username/"
        url = cls.BASE_URL + endpoint + username
        return url

    @classmethod
    def user_followers(cls, path, id):
        endpoint = "/users/{}/{}".format(id, path)
        url = cls.BASE_URL + endpoint
        return url

    @classmethod
    def user_following(cls, id):
        endpoint = "/users/{}/following".format(id)
        url = cls.BASE_URL + endpoint
        return url

    @classmethod
    def user_timeline(cls, id):
        endpoint = "/users/{}/tweets".format(id)
        return cls.BASE_URL + endpoint

    @classmethod
    def user_liked_tweets(cls, id):
        return cls.BASE_URL + "/users/{}/liked_tweets".format(id)

    @classmethod
    def tweets_lookup(cls, ids):
        param = ",".join(str(id) for id in ids)
        endpoint = "/tweets?ids={}".format(param)
        return cls.BASE_URL + endpoint

    @classmethod
    def tweet_lookup(cls, id):
        return cls.BASE_URL + "/tweets/{}".format(id)

    @classmethod
    def get_user_mentions_by_id(cls, id):
        endpoint = "/users/{}/mentions".format(id)
        url = cls.BASE_URL + endpoint
        return url

    @classmethod
    def tweet_search(cls):
        endpoint = "/tweets/search/recent"
        return cls.BASE_URL + endpoint

    @classmethod
    def create_friendship(cls, source_user_id):
        return cls.BASE_URL + f"/users/{source_user_id}/following"

    @classmethod
    def destroy_friendship(cls, source_user_id, target_user_id):
        return cls.BASE_URL + f"/users/{source_user_id}/following/{target_user_id}"

    @classmethod
    def mute_friendship(cls, source_user_id):
        return cls.BASE_URL + f"/users/{source_user_id}/muting"

    @classmethod
    def unmute_friendship(cls, source_user_id, target_user_id):
        return cls.BASE_URL + f"/users/{source_user_id}/muting/{target_user_id}"

    @classmethod
    def block_friendship(cls, source_user_id):
        return cls.BASE_URL + f"/users/{source_user_id}/blocking"

    @classmethod
    def unblock_friendship(cls, source_user_id, target_user_id):
        return cls.BASE_URL + f"/users/{source_user_id}/blocking/{target_user_id}"

    @classmethod
    def manage_tweet(cls):
        return cls.BASE_URL + "/tweets"

    # v1 endpoints
    @classmethod
    def show_user(cls):
        return cls.BASE_URL_V1 + "/users/show.json"

    @classmethod
    def friendship_lookup(cls):
        return cls.BASE_URL_V1 + "/friendships/lookup.json"

    @classmethod
    def friendship_show(cls):
        return cls.BASE_URL_V1 + f"/friendships/show.json"

    @classmethod
    def search_users(cls):
        return cls.BASE_URL_V1 + "/users/search.json"

    @classmethod
    def users_timeline(cls):
        return cls.BASE_URL_V1 + "/statuses/user_timeline.json"

    @classmethod
    def users_home_timeline(cls):
        return cls.BASE_URL_V1 + "/statuses/home_timeline.json"
