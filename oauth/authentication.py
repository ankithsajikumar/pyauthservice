import jwt
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model
from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from oauth2_provider.utils import jwk_from_pem

from pyauthservice.constants import DEFAULT_AUDIENCE


class SSOJWTAuthentication(BaseAuthentication):
    """
    Authenticate requests using JWTs issued by this SSO.
    """

    def authenticate(self, request):
        auth_header = request.headers.get("Authorization", "")
        if not auth_header or not auth_header.startswith("Bearer "):
            return None  # let other authenticators run (or AnonymousUser)

        token = auth_header.split(" ")[1]

        try:
            private_key = settings.OAUTH2_PROVIDER["OIDC_RSA_PRIVATE_KEY"]
            public_key = jwk_from_pem(private_key)
            
            payload = jwt.decode(
                token,
                public_key,
                algorithms=["RS256"],
                audience=[DEFAULT_AUDIENCE],
                issuer=settings.OAUTH2_PROVIDER["OIDC_ISS_ENDPOINT"],
            )

        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed("Token expired")
        except jwt.InvalidTokenError as e:
            raise exceptions.AuthenticationFailed(f"Invalid token: {str(e)}")

        User = get_user_model()
        user = None
        if "sub" in payload:
            try:
                user = User.objects.get(username=payload["sub"])
            except User.DoesNotExist:
                user = AnonymousUser()

        return (user, payload)
