from rest_framework.viewsets import ModelViewSet
from team.models import Team
from team.serializers import TeamSerializers


class TeamViewSet(ModelViewSet):
    serializer_class = TeamSerializers
    queryset = Team.objects.all()
