from django.db import models


class Flag(models.Model):
    created = models.DateTimeField(auto_now_add=True)
