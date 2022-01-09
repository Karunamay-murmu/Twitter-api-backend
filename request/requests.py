import requests
import asyncio
import aiohttp
import json

from django.conf import settings

from requests_oauthlib import OAuth1



class Request:

    options = {
        "method": "GET",
        "params": {},
        "data": {},
        "headers": {
            "Authorization": f"Bearer {settings.TWITTER_API_BEARER_TOKEN}",
        },
        "timeout": 10,
    }

    auth = OAuth1(
        settings.TWITTER_API_KEY,
        settings.TWITTER_API_SECRET_KEY,
        settings.TWITTER_ACCESS_TOKEN,
        settings.TWITTER_ACCESS_TOKEN_SECRET,
    )

    @classmethod
    def make(self, url, extra_options=None):
        for (k, v) in extra_options.items():
            self.options[k] = v
        async def fetch_data():
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.request(**self.options, url=url) as response:
                        res = await response.json()
                        if response.status == 200:
                            return res
                        else:
                            return res["errors"]
            finally:
                await session.close()
        return fetch_data()
        # return fetch_data()

        # response = requests.request(url=url, **self.options)
        # print(response)
        # return response.json()
