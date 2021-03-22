import requests

from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import permissions, status
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.response import Response
from rest_framework.utils import json
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from accounts.authentication import MultipleTokenAuthentication
from accounts.models import Account, AuthToken
from accounts.serializers import AccountDashboardSerializer, AccountSerializer


def index(request):
    return render(request, "accounts/base.html")


class AccountViewSet(ModelViewSet):
    serializer_class = AccountSerializer
    queryset = Account.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [MultipleTokenAuthentication]


class DashboardViewSet(ModelViewSet):
    serializer_class = AccountDashboardSerializer
    queryset = Account.objects.all()
    http_method_names = ["get", "put", "patch", "post", "head"]
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [MultipleTokenAuthentication]

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
            try:
                account = Account.objects.get(user=user)
            except Account.DoesNotExist:
                account = Account.objects.create(
                    user=user,
                    profile_pic=data["picture"],
                )

        except User.DoesNotExist:
            data_dict = {
                "username": data["email"],
                "first_name": "",
                "last_name": "",
                "email": data["email"]
            }
            
            if "given_name" in data.keys():
                data_dict["first_name"] = data["given_name"]
            
            if "family_name" in data.keys():
                data_dict["last_name"] = data["family_name"]
            
            user = User.objects.create(**data_dict)
            account = Account.objects.create(
                user=user,
                profile_pic=data["picture"],
            )

        token = AuthToken.objects.create(user=user)
        response = {}
        response["email"] = user.email
        response["user_id"] = account.id
        response["access_token"] = str(token)
        return Response(response, status=status.HTTP_200_OK)


class Logout(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [MultipleTokenAuthentication]
    http_method_names = ["get"]

    def get(self, request, *args, **kwargs):
        if request.META.get("HTTP_AUTHORIZATION") is not None:
            _, token = request.META.get("HTTP_AUTHORIZATION").split(" ")
            AuthToken.objects.get(key=token).delete()
            return Response({"Success": "Logout"}, status=status.HTTP_200_OK)
        else:
            return Response({"Error": "Token not found!"}, status=status.status.HTTP_404_NOT_FOUND)
