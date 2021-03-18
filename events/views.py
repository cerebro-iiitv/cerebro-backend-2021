from rest_framework.viewsets import ModelViewSet

from events.models import Contact, Event
from events.serializers import ContactSerializer, EventSerializer


class EventViewSet(ModelViewSet):
    serializer_class = EventSerializer
    http_method_names = ["get"]

    def get_queryset(self):
        if self.request.GET.get("type") is not None:
            event_type = self.request.GET.get("type")
            return Event.objects.filter(event_type=event_type).order_by("priority")

        return Event.objects.all().order_by("priority")


class ContactViewSet(ModelViewSet):
    serializer_class = ContactSerializer
    queryset = Contact.objects.all().order_by("priority")
