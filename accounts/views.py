import requests
from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import permissions, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.response import Response
from rest_framework.utils import json
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from accounts.models import Account
from accounts.serializers import AccountDashboardSerializer, AccountSerializer


def index(request):
    return render(request, "accounts/base.html")


class AccountViewSet(ModelViewSet):
    serializer_class = AccountSerializer
    queryset = Account.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]


class DashboardViewSet(ModelViewSet):
    serializer_class = AccountDashboardSerializer
    queryset = Account.objects.all()
    http_method_names = ["get"]
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def list(self, request):
        raise MethodNotAllowed("GET", detail="Method 'GET' not allowed without lookup")

    def retrieve(self, request, *args, **kwargs):
        account = Account.objects.get(pk=kwargs.get("pk"))
        if request.user == account.user:
            return super().retrieve(request, *args, **kwargs)
        else:
            return Response(
                {"Error": "Permission Denied"}, status=status.HTTP_401_UNAUTHORIZED
            )


class GoogleLogin(APIView):
    def post(self, request):
        payload = {"access_token": request.data.get("Token")}
        r = requests.get(
            "https://www.googleapis.com/oauth2/v2/userinfo", params=payload
        )
        data = json.loads(r.text)

        if "error" in data:
            return Response(
                {"error": "Invalid Google Token or this Token has already expired"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user = User.objects.get(email=data["email"])
        except User.DoesNotExist:
            user = User.objects.create(
                username=data["given_name"],
                first_name=data["given_name"],
                last_name=data["family_name"],
                email=data["email"],
            )
            account = Account.objects.create(
                user=user,
                profile_pic=data["picture"],
            )
        token = Token.objects.create(user=user)
        response = {}
        response["email"] = user.email
        response["user_id"] = account.id
        response["access_token"] = str(token)
        return Response(response, status=status.HTTP_200_OK)


class Logout(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    http_method_names = ["get"]

    def get(self, request, *args, **kwargs):
        if request.user.auth_token is not None:
            request.user.auth_token.delete()
            return Response({"Success": "Logout"}, status=status.HTTP_200_OK)
