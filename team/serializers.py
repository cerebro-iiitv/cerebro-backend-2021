from rest_framework import serializers
from team.models import Team


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = (
            "id",
            "name",
            "team",
            "role",
            "profilepic",
            "portfolio",
            "github",
            "linked_in",
            "twitter",
            "dribbble",
        )
