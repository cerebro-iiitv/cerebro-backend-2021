from django.db import router
from django.urls import path
from rest_framework.routers import SimpleRouter
from rest_framework.urlpatterns import format_suffix_patterns

from registration.views import TeamRegistrationViewSet, CsvGenerate, index

router = SimpleRouter()
router.register("team-register", TeamRegistrationViewSet, basename="api-team")


urlpatterns = [
    path("", index, name="index"),
    path("csv-generate/<int:pk>", CsvGenerate.as_view(), name="csv-generate"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
urlpatterns += router.urls
