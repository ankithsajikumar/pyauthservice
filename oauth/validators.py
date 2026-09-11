from django.core.exceptions import ImproperlyConfigured
from oauthlib.oauth2.rfc6749 import errors
from oauth2_provider.oauth2_validators import OAuth2Validator


class UserClaimsValidator(OAuth2Validator):
    def finalize_id_token(self, id_token, token, token_handler, request):
        try:
            request.client.jwk_key
        except ImproperlyConfigured as exc:
            raise errors.InvalidClientError(
                description=f'OAuth client signing configuration is invalid: {exc}'
            ) from exc
        return super().finalize_id_token(id_token, token, token_handler, request)

    def get_additional_claims(self, request):
        user = request.user
        return {
            'email': user.email,
            'email_verified': bool(user.email),
            'name': user.get_full_name(),
            'given_name': user.first_name,
            'family_name': user.last_name,
            'preferred_username': user.get_username(),
        }