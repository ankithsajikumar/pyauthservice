import time, uuid, jwt, hashlib, base64
from django.conf import settings
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

from pyauthservice.constants import DEFAULT_AUDIENCE

def _get_public_key(private_key_pem: str):
    private_key = serialization.load_pem_private_key(
        private_key_pem.encode(),
        password=None,
        backend=default_backend()
    )
    return private_key.public_key()

def _generate_kid(public_key) -> str:
    pub_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    digest = hashlib.sha256(pub_pem).digest()
    return base64.urlsafe_b64encode(digest[:30]).decode().rstrip("=")

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
    public_key = _get_public_key(private_key)
    kid = _generate_kid(public_key)
    return jwt.encode(payload, private_key, algorithm="RS256", headers={"kid": kid})
