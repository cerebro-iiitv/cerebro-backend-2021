from rest_framework import serializers

from accounts.models import Account
from registration.models import TeamMember


class AccountSerializer(serializers.ModelSerializer):
    

    class Meta:
        model = Account
        fields = "__all__"


class RegisteredEventSerializer(serializers.ModelSerializer):
    event_name = serializers.CharField(source="event.title")
    team_code = serializers.CharField(source="team.team_code")
    start_time = serializers.CharField(source="event.start_time")
    end_time = serializers.CharField(source="event.end_time")

    class Meta:
        model = TeamMember
        fields = ["event_name", "team_code", "start_time", "end_time", "id"]


class AccountDashboardSerializer(serializers.ModelSerializer):
    user_team = RegisteredEventSerializer(many=True)
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    email = serializers.CharField(source="user.email")

    class Meta:
        model = Account
        fields = ["first_name", "last_name", "email", "mobile_number", "profile_pic", "user_team"]
