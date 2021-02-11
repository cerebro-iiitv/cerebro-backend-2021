from rest_framework import serializers
from events.models import Event, Contact


class ContactSerializers(serializers.ModelSerializer):

    class Meta:
        model = Contact
        fields = '__all__'


class EventSerializers(serializers.ModelSerializer):

    EventContact = ContactSerializers(many=True)

    class Meta:
        model = Event
        fields = '__all__'