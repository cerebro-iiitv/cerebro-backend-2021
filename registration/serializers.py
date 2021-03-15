from rest_framework import serializers
from accounts.models import Account
from .models import TeamMember


class TeamMemberSerializer(serializers.ModelSerializer):
    event_name = serializers.CharField(source="event.title")
    team_code = serializers.CharField(source="team.team_code")

    class Meta:
        model = TeamMember
        fields = ["event_name", "team_code"]


class AccountDashboardSerializer(serializers.ModelSerializer):
    user_team = TeamMemberSerializer(many=True)

    class Meta:
        model = Account
        fields = "__all__"
