from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

app_name = "accounts"
urlpatterns = [
    path("", views.index, name="index"),
    path("googlelogin/", views.GoogleLogin.as_view(), name="googlelogin"),
    path("logout/", views.Logout.as_view(), name="logout"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
