import requests
from django.shortcuts import render
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.utils import json
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.authentication import TokenAuthentication

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


class GoogleLogin(APIView):
    def post(self, request):
        payload = {"access_token": request.data.get("Token")}
        r = requests.get(
            "https://www.googleapis.com/oauth2/v2/userinfo", params=payload
        )
        data = json.loads(r.text)

        if "error" in data:
            return Response(
                {"error": "invalid google token or this token has already expired"},
                status=status.HTTP_200_OK,
            )

        try:
            user = Account.objects.get(email=data["email"])
        except Account.DoesNotExist:
            user = Account.objects.create(
                email=data["email"],
                first_name=data["given_name"],
                last_name=data["family_name"],
                profile_pic=data["picture"],
            )
        token = RefreshToken.for_user(user)
        response = {}
        response["email"] = user.email
        response["user_id"] = user.id
        response["access_token"] = str(token.access_token)
        response["refresh_token"] = str(token)
        return Response(response, status=status.HTTP_200_OK)
