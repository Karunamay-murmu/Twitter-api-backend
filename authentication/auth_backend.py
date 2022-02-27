from urllib import request
from jose import jwt

from social_core.backends.oauth import BaseOAuth2


class Auth0(BaseOAuth2):
    name = "auth0"
    SCOPE_SEPARATOR = " "
    ACCESS_TOKEN_METHOD = "POST"
    REDIRECT_STATE = False
    EXTRA_DATA = [
        ("picture", "picture"),
        ("email", "email"),
    ]

    def authorization_url(self):
        return f"{self.setting('DOMAIN')}/authorize"

    def access_token_url(self):
        return f"{self.setting('DOMAIN')}/oauth/token"

    def get_user_details(self, response):
        id_token = response.get("id_token")
        jwks = request.urlopen(f"{self.setting('DOMAIN')}/.well-known/jwks.json" )
        issuer = f"{self.setting('DOMAIN')}/"
        audience = self.setting("KEY")
        payload = jwt.decode(
            id_token,
            jwks.read(),
            algorithms=["RS256"],
            audience=audience,
            issuer=issuer,
        )
        return {
            "username": payload["nickname"],
            "first_name": payload["name"],
            "picture": payload["picture"],
            "user_id": payload["sub"],
        }