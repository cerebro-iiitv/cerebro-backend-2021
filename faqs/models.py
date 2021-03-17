from django.db import models


class Faq(models.Model):
    question = models.TextField(blank=False)
    answer = models.TextField(blank=False)

    def __str__(self):
        return self.question
