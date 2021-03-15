from django.db import router
from django.urls import path
from rest_framework.routers import SimpleRouter
from rest_framework.urlpatterns import format_suffix_patterns

from .views import TeamRegistrationViewSet, index

router = SimpleRouter()
router.register("team-register", TeamRegistrationViewSet, basename="api-team")


urlpatterns = [path("", index, name="index")]

urlpatterns = format_suffix_patterns(urlpatterns)
urlpatterns += router.urls
