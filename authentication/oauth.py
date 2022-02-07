from django.conf import settings

CLIENT_ID = settings.OAUTH_CLIENT_ID
REDIRECT_URI = settings.OAUTH_REDIRECT_URI

scope_list = [
    "offline.access",
    "tweet.read",
    "tweet.write",
    "tweet.moderate.write",
    "users.read",
    "follows.read",
    "follows.write",
    "offline.access",
    "space.read",
    "mute.read",
    "mute.write",
    "like.read",
    "like.write",
    "list.read",
    "list.write",
    "block.read",
    "block.write"
]

scope = "+".join(scope_list)

authorize_url = f"https://twitter.com/i/oauth2/authorize?response_type=code&client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&scope={scope}&state=state&code_challenge=challenge&code_challenge_method=plain"


# https://twitter.com/i/oauth2/authorize?response_type=code&client_id=YUQ4NDFKVXNCSUxKWVlNMF9SWXM6MTpjaQ&redirect_uri=https://www.example.com&scope=tweet.read%20users.read%20follows.read%20follows.write&state=state&code_challenge=challenge&code_challenge_method=plain