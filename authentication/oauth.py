import requests
import jwt

from requests_oauthlib import OAuth1, OAuth1Session
from urllib.parse import parse_qs

from django.conf import settings


class OAuth:

    api_key = settings.TWITTER_API_KEY
    api_secret_key = settings.TWITTER_API_SECRET_KEY
    # callback_url = "http://127.0.0.1:8000/2/oauth2/callback"
    callback_url = "http://localhost:3000/login"
    scope = "+".join([
        "offline.access", "tweet.read", "tweet.write", "tweet.moderate.write",
        "users.read", "follows.read", "follows.write", "offline.access",
        "space.read", "mute.read", "mute.write", "like.read", "like.write",
        "list.read", "list.write", "block.read", "block.write"
    ])
    oauth_token = None
    oauth_token_secret = None
    oauth_callback_confirmed = False

    def __init__(self):
        self.oauth = OAuth1(self.api_key, self.api_secret_key)

    def encode_token(self, payload):
        key = self.api_key
        return jwt.encode(payload=payload, key=key, algorithm="HS256")

    def decode_token():
        ...

    def get_request_token(self):
        url = "https://api.twitter.com/oauth/request_token"
        data = {"oauth_callback": self.callback_url}
        try:
            response = requests.post(url=url, data=data, auth=self.oauth)
            if response.status_code == 200:
                credentials = parse_qs(response.content.decode())
                self.oauth_token = credentials.get("oauth_token", [None])[0]
                self.oauth_token_secret = credentials.get(
                    "oauth_token_secret", [None])[0]
                self.oauth_callback_confirmed = credentials.get(
                    "oauth_callback_confirmed", [None])[0]
                return {
                    "oauth_token": self.oauth_token,
                    "oauth_token_secret": self.oauth_token_secret,
                    "oauth_callback_confirmed": self.oauth_callback_confirmed
                }
            else:
                error = response.json()["errors"][0]
                raise Exception(error["message"])
        except Exception as e:
            return e

    def make_authorize_url(self, oauth_token):
        if oauth_token == self.oauth_token and self.oauth_callback_confirmed:
            return "https://api.twitter.com/oauth/authorize?oauth_token={}".format(
                oauth_token)
        else:
            raise Exception("Invalid oauth_token")

    def get_oauth_token(self):
        if not self.oauth_token:
            return Exception("oauth authentication hasn't initialized yet")
        else:
            return self.oauth_token

    def get_access_token(self, oauth_token, oauth_verifier):
        url = "https://api.twitter.com/oauth/access_token"
        oauth = OAuth1(
            client_key=self.api_key,
            resource_owner_key=oauth_token,
            verifier=oauth_verifier,
        )
        try:
            response = requests.post(url=url, auth=oauth)
            if response.status_code == 200:
                credentials = parse_qs(response.content.decode())
                print(credentials)
                return {**credentials}
            else:
                error = response.json()["errors"][0]
                raise Exception(error["message"])
        except Exception as e:
            return e


oauth_session = OAuth()