from django.db import models
from django.db.models import fields
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

class TeamRegisterSerializer(serializers.Serializer):
    account_id = serializers.IntegerField(required = True)
    event_id = serializers.IntegerField(required = True)
    team_code = serializers.CharField(default = None)