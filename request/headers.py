from django.conf import settings

REQUEST_HEADER = {
    "Accept": "text/html,application/json,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-us",
    "Connection": "keep-alive",
    "Access-Control-Allow-Origin": "*",
    "Authorization": f"Bearer {settings.TWITTER_API_BEARER_TOKEN}",
}
