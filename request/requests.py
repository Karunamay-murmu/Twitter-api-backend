import asyncio
import aiohttp

from django.conf import settings

import oauthlib.oauth1

from users.models import Account


def get_user_object(id):
    try:
        user = Account.objects.get(twitter_user_id=id)
        return user
    except Account.DoesNotExist:
        raise Exception("User not found")


class Request:
    @staticmethod
    def oauth_session(access_token, access_token_secret):
        twitter_oauth = oauthlib.oauth1.Client(
            client_key=settings.TWITTER_API_KEY,
            client_secret=settings.TWITTER_API_SECRET_KEY,
            resource_owner_key=access_token,
            resource_owner_secret=access_token_secret,
        )
        return twitter_oauth

    @staticmethod
    def request_options(options, extra_options):
        new_options = {**options}
        if extra_options:
            for (key, value) in extra_options.items():
                if key == "method" and value == "POST":
                    del new_options["headers"]["Authorization"]
                    new_options["headers"]["Content-Type"] = "application/json"
                new_options[key] = value
        return new_options

    @classmethod
    def make(cls, url, options={}, access_token=None, access_token_secret=None):
        async def fetch_data():
            uri = url
            method = options.get("method", "GET")
            body = options.get("body", None)
            params = options.get("params", {})
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {settings.TWITTER_API_BEARER_TOKEN}",
            }
            if options.get("headers", None):
                headers.update(options["headers"])
            try:
                res = None
                async with aiohttp.ClientSession() as session:
                    if access_token and access_token_secret:
                        oauth = cls.oauth_session(access_token, access_token_secret)
                        uri, headers, body = oauth.sign(
                            uri=uri,
                            http_method=method,
                            body=body,
                            headers=headers,
                        )
                    async with session.request(
                        url=uri,
                        method=method,
                        headers=headers,
                        data=body,
                        params=params,
                        timeout=20,
                    ) as response:
                        res = await response.json()
                        if response.status == 200:
                            return {
                                "response": res,
                                "status": response.status,
                            }
                    return {"response": res, "status": response.status}
            except (aiohttp.ClientError, asyncio.TimeoutError) as e:
                raise Exception("Error occured while fetching data")

            finally:
                await session.close()

        return fetch_data()
