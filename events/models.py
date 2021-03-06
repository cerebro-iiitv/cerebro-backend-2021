from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Event(models.Model):
    priority = models.IntegerField(blank=True)
    event = models.CharField(max_length=100, blank=False)
    description = models.CharField(max_length=2000, blank=True)
    prize = models.CharField(max_length=20, blank=True)
    team_size = models.CharField(max_length=20, blank=True)
    start_time = models.CharField(max_length=100, blank=False)
    end_time = models.CharField(max_length=100, blank=False)
    about = models.CharField(max_length=1500, blank=True)
    rules_doc = models.FileField(upload_to="rules", blank=True)

    def __str__(self):
        return self.event


class Contact(models.Model):

    ROLE_CHOICES = [
        ("Converner", "Converner"),
        ("Co_Converner1", "Co_Converner1"),
        ("Co_Converner2", "Co_Converner2"),
        ("Member1", "Member1"),
        ("Member2", "Member2"),
    ]

    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, related_name="EventContact"
    )
    name = models.CharField(max_length=100, blank=False)
    role = models.CharField(max_length=15, choices=ROLE_CHOICES)
    phone_number = PhoneNumberField(blank=True)

    def __str__(self):
        return self.name