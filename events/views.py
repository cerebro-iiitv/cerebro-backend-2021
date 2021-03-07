from rest_framework import decorators, response, status
from rest_framework.viewsets import ModelViewSet

from events.models import Contact, Event
from events.serializers import ContactSerializer, EventSerializer


class EventViewSet(ModelViewSet):
    serializer_class = EventSerializer

    def get_queryset(self):
        if self.request.GET.get("type") is not None:
            event_type = self.request.GET.get("type")
            return Event.objects.filter(event_type=event_type).order_by("priority")

        return Event.objects.all().order_by("priority")

    @decorators.action(detail=True, methods=["GET"])
    def contacts(self, request, pk=None):
        event = self.get_object()
        contacts = Contact.objects.filter(event=event)
        contacts_data = ContactSerializer(
            instance=contacts, many=True, context={"request": request}
        ).data

        return response.Response(contacts_data, status=status.HTTP_200_OK)


class ContactViewSet(ModelViewSet):
    serializer_class = ContactSerializer
    queryset = Contact.objects.all().order_by("priority")
