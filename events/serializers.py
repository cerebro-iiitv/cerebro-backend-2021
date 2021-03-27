from rest_framework import serializers

from events.models import Contact, Event


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ("id", "name", "role", "phone_number")


class EventSerializer(serializers.ModelSerializer):
    contacts = serializers.SerializerMethodField()

    def get_contacts(self, obj: Event):
        contacts = obj.events.all().order_by("priority")

        return ContactSerializer(contacts, many=True).data

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
            "social_media",
            "is_closed",
            "contacts",
        )
