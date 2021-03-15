from rest_framework import serializers
from accounts.models import Account
from .models import TeamMember

class TeamMemberSerializer(serializers.ModelSerializer):
    team_code = serializers.CharField(required = False, source='team.team_code')

    class Meta:
        model = TeamMember
        fields = ['account', 'event', 'team_code']


