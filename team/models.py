from django.db import models


ROLE_CHOICES = [
    ("Student Convener", "Student Convenor"),
    ("Technical Lead", "Technical Lead"),
    ("Convener", "Convener"),
    ("Head", "Head"),
    ("Co-Head", "Co-Head"),
    ("Member", "Member"),
]

TEAM_CHOICES = [
    ("Core", "Core"),
    ("Core Support", "Core Support"),
    ("Development", "Web Dev"),
    ("Design", "Design"),
    ("Video Editing", "Video Editing"),
    ("PR", "PR"),
    ("Gaming", "Gaming"),
]


class Team(models.Model):
    name = models.CharField(max_length=100, blank=False)
    team = models.CharField(max_length=100, choices=TEAM_CHOICES)
    role = models.CharField(max_length=100, blank=False, choices=ROLE_CHOICES)
    profilepic = models.ImageField(upload_to="team-profilepics", blank=True)
    portfolio = models.URLField(blank=True)
    github = models.URLField(blank=True)
    linked_in = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    dribble = models.URLField(blank=True)
