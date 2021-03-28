from django.db import models

from accounts.models import Account
from events.models import Event


class Dashboard(models.Model):
    event_name = models.CharField(max_length=100, blank=True)
    starts_on = models.DateTimeField()
    action = models.BooleanField(default=True)


class TeamStatus(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="reg_team")
    current_size = models.IntegerField(default=1)
    is_full = models.BooleanField(default=False)
    team_code = models.CharField(max_length=15, default=None)

    def __str__(self):
        return self.team_code


class TeamMember(models.Model):
    account = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name="user_team"
    )
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="member")
    team = models.ForeignKey(
        TeamStatus, on_delete=models.CASCADE, related_name="team_member"
    )

    def __str__(self) -> str:
        return self.event.title + " | " + self.team.team_code
