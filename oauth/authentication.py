import jwt
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model
from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from cryptography.hazmat.primitives import serialization
import logging

from pyauthservice.constants import DEFAULT_AUDIENCE

logger = logging.getLogger(__name__)


class SSOJWTAuthentication(BaseAuthentication):
    """
    Authenticate requests using JWTs issued by this SSO.
    """

    def authenticate(self, request):
        auth_header = request.headers.get("Authorization", "")
        if not auth_header or not auth_header.startswith("Bearer "):
            logger.warning("Authorization header missing or invalid")
            return None  # let other authenticators run (or AnonymousUser)

        token = auth_header.split(" ")[1]

        try:
            # Load public key from private key
            private_key = settings.OAUTH2_PROVIDER["OIDC_RSA_PRIVATE_KEY"]
            public_key = serialization.load_pem_private_key(
                private_key.encode(),
                password=None,
            ).public_key()
            public_key_pem = public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo,
            ).decode()

            # Decode the token
            payload = jwt.decode(
                token,
                public_key_pem,
                algorithms=["RS256"],
                audience=[DEFAULT_AUDIENCE],
                issuer=settings.OAUTH2_PROVIDER["OIDC_ISS_ENDPOINT"],
            )
        except jwt.ExpiredSignatureError:
            logger.error("Token expired")
            raise exceptions.AuthenticationFailed("Token expired")
        except jwt.InvalidTokenError as e:
            logger.error(f"Invalid token: {str(e)}")
            raise exceptions.AuthenticationFailed(f"Invalid token: {str(e)}")

        # Get user from the token payload
        User = get_user_model()
        user = None
        if "sub" in payload:
            try:
                user = User.objects.get(username=payload["sub"])
            except User.DoesNotExist:
                user = AnonymousUser()

        return (user, payload)
