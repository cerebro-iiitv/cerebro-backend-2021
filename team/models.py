from django.db import models


ROLE_CHOICES = [
    ("President", "President"),
    ("Student Convenor", "Student Convenor"),
    ("Technical Lead", "Technical Lead"),
    ("Technical Co-Lead", "Technical Co-Lead"),
    ("Convenor", "Convenor"),
    ("Head", "Head"),
    ("Co-Head", "Co-Head"),
    ("Member", "Member"),
]

TEAM_CHOICES = [
    ("core", "Core"),
    ("core-support", "Core Support"),
    ("web", "Web Dev"),
    ("design", "Design"),
    ("video-editing", "Video Editing"),
    ("pr", "PR"),
    ("gaming", "Gaming"),
]


class Team(models.Model):
    priority = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=100, blank=False)
    team = models.CharField(max_length=100, choices=TEAM_CHOICES)
    role = models.CharField(max_length=100, blank=False, choices=ROLE_CHOICES)
    profilepic = models.ImageField(upload_to="team-profilepics", blank=True)
    portfolio = models.URLField(blank=True)
    github = models.URLField(blank=True)
    linked_in = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    dribbble = models.URLField(blank=True)

    def __str__(self):
        return self.team + " | " + self.name

    def save(self, *args, **kwargs):
        if self.role == "President":
            self.priority = 1

        elif (
            self.role == "Student Convenor"
            or self.role == "Technical Lead"
            or self.role == "Head"
        ):
            self.priority = 2

        elif self.role == "Co-Head":
            self.priority = 3

        elif self.role == "Member":
            self.priority = 4

        super(Team, self).save(*args, **kwargs)
