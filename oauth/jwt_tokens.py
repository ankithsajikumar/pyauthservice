import time, uuid, jwt
from django.conf import settings

from pyauthservice.constants import DEFAULT_AUDIENCE

def jwt_access_token_generator(request):
    now = int(time.time())
    exp = now + settings.OAUTH2_PROVIDER.get("ACCESS_TOKEN_EXPIRE_SECONDS", 3600)

    # Default audience
    audiences = [DEFAULT_AUDIENCE]

    payload = {
        "iss": settings.OAUTH2_PROVIDER["OIDC_ISS_ENDPOINT"],
        "sub": str(getattr(request, "user", getattr(request, "client_id", "")) or ""),
        "aud": audiences,
        "iat": now,
        "exp": exp,
        "jti": str(uuid.uuid4()),
        "client_id": getattr(request, "client_id", None),
        "scope": " ".join(request.scopes or []),
        "grant_type": getattr(request, "grant_type", ""),
    }

    private_key = settings.OAUTH2_PROVIDER["OIDC_RSA_PRIVATE_KEY"]
    return jwt.encode(payload, private_key, algorithm="RS256")
