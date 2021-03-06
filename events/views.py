from rest_framework.viewsets import ModelViewSet

from events.models import Contact, Event
from events.serializers import ContactSerializers, EventSerializers


class EventViewSets(ModelViewSet):
    serializer_class = EventSerializers
    queryset = Event.objects.all()


class ContactViewSets(ModelViewSet):
    serializer_class = ContactSerializers
    queryset = Contact.objects.all()
