from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import status
from rest_framework.utils import json
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from accounts.serializers import AccountSerializers
from accounts.models import Account
import requests


def index(request):
    return render(request, 'accounts/base.html')


class AccountViewSets(ModelViewSet):
    serializer_class = AccountSerializers
    queryset = Account.objects.all()


class GoogleLogin(APIView):
    def post(self, request):
        payload = {'access_token': request.data.get('Token')}
        r = requests.get('https://www.googleapis.com/oauth2/v2/userinfo', params=payload)
        data = json.loads(r.text)
        print(data)

        if 'error' in data:
            return Response({'error': 'invalid google token or this token has already expired'}, status=status.HTTP_200_OK)

        try:
            user = Account.objects.get(email=data['email'])
        except Account.DoesNotExist:
            return Response({'Account not found': 'user with given account does not exist'})
        
        token = RefreshToken.for_user(user)
        response = {}
        response['email'] = user.email
        response['access_token'] = str(token.access_token)
        response['refresh_token'] = str(token)
        return Response(response, status=status.HTTP_200_OK)
        

