import requests
from requests_oauthlib import OAuth1

from django.conf import settings

class Request:

    options = {
        "method": "GET",
        "params": {},
        "data": {},
        "headers": {
            "Authorization": f"Bearer {settings.TWITTER_API_BEARER_TOKEN}",
        },
        "timeout": (5, 10),
    }

    auth = OAuth1(settings.TWITTER_API_KEY, settings.TWITTER_API_SECRET_KEY, settings.TWITTER_ACCESS_TOKEN, settings.TWITTER_ACCESS_TOKEN_SECRET)


    @classmethod
    def make(self, url, extra_options=None):
        for (k, v) in extra_options.items():
            self.options[k] = v

        response = requests.request(url=url, auth=self.auth, **self.options)
        return response.json()
