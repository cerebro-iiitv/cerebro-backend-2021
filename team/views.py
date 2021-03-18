from rest_framework.viewsets import ModelViewSet

from team.models import Team
from team.serializers import TeamSerializer


class TeamViewSet(ModelViewSet):
    serializer_class = TeamSerializer
    http_method_names = ["get"]

    def get_queryset(self):
        if self.request.GET.get("team") is not None:
            team = self.request.GET.get("team")
            return Team.objects.filter(team=team).order_by("priority")

        return Team.objects.all().order_by("priority")
