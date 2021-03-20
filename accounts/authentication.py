from rest_framework.authentication import TokenAuthentication
from accounts.models import AuthToken
from rest_framework.exceptions import AuthenticationFailed

class ExpiringTokenAuthentication(TokenAuthentication):
    '''
    Expiring token for mobile and desktop clients.
    It expires every 24hrs requiring client to supply valid username 
    and password for new one to be created.
    '''
    def authenticate_credentials(self, key, request=None):
        models = self.get_model()
        try:
            token = models.objects.select_related('user').get(key=key)
        except models.DoesNotExist:
            raise AuthenticationFailed({'error':'Invalid or Inactive Token', 'is_authenticated': False})
 
        if not token.user.is_active:
            raise AuthenticationFailed({'error':'Invalid user', 'is_authenticated': False})
 
        return token.user, token