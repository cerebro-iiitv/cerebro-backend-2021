from django.db import router
from django.urls import path
from rest_framework import views
from .views import index, DashboardViewSets, TeamViewSets
from rest_framework.routers import SimpleRouter
from rest_framework.urlpatterns import format_suffix_patterns

router = SimpleRouter()
router.register("dashboard", DashboardViewSets,
                basename='api-dashboard')
router.register("team_register", TeamViewSets,
                basename='api-team')


urlpatterns = [
    path('', index, name='index')
]

urlpatterns = format_suffix_patterns(urlpatterns)
urlpatterns += router.urls