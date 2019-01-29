from django.core.exceptions import ValidationError
from rest_framework import exceptions, permissions, authentication

from api.models import APIClient


def validate_authkey(value):
    """Raises a ValidationError if value has not length 32"""
    if not len(value) == 32:
        raise ValidationError(
            'Value must be a string containing 32 alphanumeric characters')


class APIClientAuthentication(authentication.BaseAuthentication):
    
    def authenticate(self, request):
        accesskey = request.query_params.get('accesskey')
        secretkey = request.META.get('secretkey')

        # validate that AK and SK were given
        if not accesskey or not secretkey:
            return None

        # validate that AK and SK are valids
        for key in [accesskey, secretkey]:
            try:
                validate_authkey(key)
            except ValidationError:
                raise exceptions.AuthenticationFailed('Invalid APIClient credentials')

        # validate that APIClient exists for given AK and SK
        try:
            api_client = APIClient.objects.get(accesskey=accesskey, secretkey=secretkey)
            if api_client.is_active:
                return (api_client, None)
            else:
                raise api_client.DoesNotExist
        except APIClient.DoesNotExist:
            raise exceptions.AuthenticationFailed('Invalid APIClient credentials')
