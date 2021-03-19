from django.db import models
from django.contrib.auth.models import User


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile_number = models.CharField(max_length=12, blank=True)
    profile_pic = models.URLField(blank=True)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name
