from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Event(models.Model):

    EVENT_TYPE_CHOICES = [
        ("tech", "Technical"),
        ("gaming", "Gaming"),
        ("design-photo", "Design and Photography"),
        ("lit", "Literature"),
    ]

    priority = models.IntegerField(blank=True, null=True)
    event_type = models.CharField(max_length=30, choices=EVENT_TYPE_CHOICES)
    title = models.CharField(max_length=100, blank=False)
    short_name = models.CharField(max_length=4, blank=True)
    description = models.TextField(blank=True)
    prize = models.CharField(max_length=20, blank=True)
    team_size = models.IntegerField(default=1)
    start_time = models.CharField(max_length=100, blank=False)
    end_time = models.CharField(max_length=100, blank=False)
    rules_doc = models.URLField(blank=True)
    social_media = models.URLField(null=True, blank=True)
    is_closed = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Contact(models.Model):

    ROLE_CHOICES = [
        ("Convenor", "Convenor"),
        ("Co-Convenor1", "Co_Convenor1"),
        ("Co-Convenor2", "Co_Convenor2"),
        ("Member1", "Member1"),
        ("Member2", "Member2"),
    ]

    priority = models.IntegerField(blank=True, null=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="events")
    name = models.CharField(max_length=100, blank=False)
    role = models.CharField(max_length=15, choices=ROLE_CHOICES, blank=False)
    phone_number = PhoneNumberField(blank=True)

    def __str__(self):
        return self.event.title + " | " + self.name

    def save(self, *args, **kwargs):
        if self.role == "Convenor":
            self.priority = 1

        elif self.role == "Co-Convenor1" or self.role == "Co-Convenor2":
            self.priority = 2

        elif self.role == "Member1" or self.role == "Member2":
            self.priority = 3

        super(Contact, self).save(*args, **kwargs)