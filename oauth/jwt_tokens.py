import time, uuid, jwt
from django.conf import settings
from oauth2_provider.utils import jwk_from_pem

from pyauthservice.constants import DEFAULT_AUDIENCE

def get_token_user(request):
    if getattr(request, "user", ""):
        return request.user.get_username()
    elif getattr(request, "client", "") and getattr(request.client, "user", ""):
        return request.client.user.get_username()
    return ""


def jwt_access_token_generator(request):
    now = int(time.time())
    exp = now + settings.OAUTH2_PROVIDER.get("ACCESS_TOKEN_EXPIRE_SECONDS", 3600)

    # Default audience
    audiences = [DEFAULT_AUDIENCE]

    payload = {
        "iss": settings.OAUTH2_PROVIDER["OIDC_ISS_ENDPOINT"],
        "sub": get_token_user(request),
        "aud": audiences,
        "iat": now,
        "exp": exp,
        "jti": str(uuid.uuid4()),
        "client_id": getattr(request, "client_id", None),
        "scope": " ".join(request.scopes or []),
        "grant_type": getattr(request, "grant_type", ""),
    }

    private_key = settings.OAUTH2_PROVIDER["OIDC_RSA_PRIVATE_KEY"]
    key = jwk_from_pem(private_key)
    kid = key.thumbprint()
    return jwt.encode(payload, private_key, algorithm="RS256", headers={"kid": kid})
