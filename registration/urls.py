from django.db import router
from django.urls import path
from rest_framework import views
from .views import index, RegisterTeamView, DashboardViewSets
from rest_framework.routers import SimpleRouter
from rest_framework.urlpatterns import format_suffix_patterns

router = SimpleRouter()
router.register("dashboard", DashboardViewSets,
                basename='api-dashboard')


urlpatterns = [
    path('', index, name='index'),
    path('registerteam/', RegisterTeamView.as_view(), name='registerteam')
]

urlpatterns = format_suffix_patterns(urlpatterns)
urlpatterns += router.urls