from django.db import models
from django.contrib.auth.models import User
from six import MAXSIZE, python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile_number = models.CharField(max_length=12, blank=True)
    profile_pic = models.URLField(blank=True)
    institute = models.CharField(max_length=225, blank=True, null=True)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name


class AuthToken(Token):
    key = models.CharField(_("Key"), max_length=40, db_index=True, unique=True)

    # Relation to user is a ForeignKey, so each user can have more than one token
    user = models.ForeignKey(
        User,
        related_name="auth_tokens",
        on_delete=models.CASCADE,
        verbose_name=_("User"),
    )