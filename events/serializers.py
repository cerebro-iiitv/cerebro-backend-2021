from rest_framework import serializers

from events.models import Contact, Event


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = (
            "id",
            "event_type",
            "title",
            "description",
            "prize",
            "team_size",
            "start_time",
            "end_time",
            "rules_doc",
        )


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ("id", "name", "role", "phone_number")
