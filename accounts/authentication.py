from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed

from accounts.models import AuthToken


class MultipleTokenAuthentication(TokenAuthentication):
    model = AuthToken
