from django.db import models


class MeetingModel(models.Model):
    meeting_id = models.CharField(default="", max_length=255)
    created = models.DateTimeField(auto_now_add=True)
