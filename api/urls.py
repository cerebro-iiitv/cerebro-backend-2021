from accounts.views import DashboardViewSet
from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path
from events.views import ContactViewSet, EventViewSet
from faqs.views import FaqViewSet
from rest_framework.routers import SimpleRouter
from team.views import TeamViewSet

from . import views

router = SimpleRouter()

router.register("teams", TeamViewSet, basename="api-team")
router.register("events", EventViewSet, basename="api-events")
router.register("contacts", ContactViewSet, basename="api-contact")
router.register("faqs", FaqViewSet, basename="api-faqs")
router.register("dashboard", DashboardViewSet, basename="api-dashboard")

urlpatterns = [
    path("", views.landing_page, name="landing"),
    path("admin/", admin.site.urls),
    path("account/", include("accounts.urls")),
    path("registration/", include("registration.urls")),
]

urlpatterns += router.urls

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
