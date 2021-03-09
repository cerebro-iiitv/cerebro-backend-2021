from rest_framework import serializers
from accounts.models import Account
from .models import TeamMember

class TeamMemberSerializers(serializers.ModelSerializer):
    event_name = serializers.CharField(source='event.event')
    team_code = serializers.CharField(source='team.team_code')

    class Meta:
        model = TeamMember
        fields = ['event_name', 'team_code']

class AccountDashboardSerializers(serializers.ModelSerializer):
    user_team = TeamMemberSerializers(many=True)

    class Meta:
        model = Account
        fields = '__all__'

class TeamMemberSerializers(serializers.ModelSerializer):
    team_code = serializers.CharField(required = False, source='team.team_code')

    class Meta:
        model = TeamMember
        fields = ['account', 'event', 'team_code']