from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter()
router.register("events", views.EventViewSets, basename="api-event")
router.register("contact", views.ContactViewSets, basename="api-contact")


urlpatterns = router.urls
