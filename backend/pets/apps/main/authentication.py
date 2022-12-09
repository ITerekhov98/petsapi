from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from rest_framework import authentication
from rest_framework import exceptions


class CustomTokenAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_token = request.headers.get('X-Api-Key')
        if not auth_token:
            raise exceptions.NotAuthenticated('Missed API token.')
        if auth_token != settings.API_ACCESS_TOKEN: 
            raise exceptions.AuthenticationFailed('Invalid token.')
        
        return (AnonymousUser(), None) 
