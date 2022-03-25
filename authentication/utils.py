import json
import jwt
import requests
from django.contrib.auth import authenticate
from django.conf import settings


def jwt_get_username_from_payload_handler(payload):
    username = payload.get("sub").replace("|", ".")
    authenticate(remote_user=username)
    return username


def jwt_decode_token(token):
    header = jwt.get_unverified_header(token)
    jwks = requests.get(
        settings.SOCIAL_AUTH_AUTH0_DOMAIN + "/.well-known/jwks.json"
    ).json()
    public_key = None
    for jwk in jwks["keys"]:
        if jwk["kid"] == header["kid"]:
            public_key = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(jwk))

    if public_key is None:
        raise Exception("Public key not found.")

    issuer = settings.SOCIAL_AUTH_AUTH0_DOMAIN + "/"
    return jwt.decode(
        token,
        public_key,
        audience=settings.SOCIAL_AUTH_AUTH0_AUDIENCE,
        issuer=issuer,
        algorithms=["RS256"],
    )


def get_token_auth_header(request):
    auth = request.headers.get("Authorization", None)

    if not auth:
        raise Exception("Authorization header is expected")
    else:
        prifix, token = auth.split()
        if prifix != "Bearer" or not token:
            raise Exception("Incorrect authorization header")
        return token
