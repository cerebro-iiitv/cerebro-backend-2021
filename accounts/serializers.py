from django.db.models import fields
from accounts.models import Account
from rest_framework import serializers

class AccountSerializers(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = '__all__'
