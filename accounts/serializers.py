from accounts.models import Account
from rest_framework import serializers
from registration.models import TeamMember

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = "__all__"


class RegisteredEventSerializer(serializers.ModelSerializer):
    event_name = serializers.CharField(source="event.title")
    team_code = serializers.CharField(source="team.team_code")

    class Meta:
        model = TeamMember
        fields = ["event_name", "team_code"]


class AccountDashboardSerializer(serializers.ModelSerializer):
    user_team = RegisteredEventSerializer(many=True)

    class Meta:
        model = Account
        fields = "__all__"