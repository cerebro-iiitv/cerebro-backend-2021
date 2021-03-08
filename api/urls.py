from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path
from rest_framework.routers import SimpleRouter

from events.views import ContactViewSet, EventViewSet
from team.views import TeamViewSet
from accounts.views import AccountViewSet
from . import views

router = SimpleRouter()

router.register("teams", TeamViewSet, basename="api-team")
router.register("accounts", AccountViewSet, basename="api-account")
router.register("events", EventViewSet, basename="api-events")
router.register("contacts", ContactViewSet, basename="api-contact")

urlpatterns = [
    path("", views.landing_page, name="landing"),
    path("admin/", admin.site.urls),
    path("account/", include("accounts.urls")),
    path('registration/', include('registration.urls')),
    path('events/', include('events.urls')),
    path('team/', include('team.urls')),
]

urlpatterns += router.urls

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
