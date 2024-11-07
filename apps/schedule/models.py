from django.contrib.auth import get_user_model
from django.db import models

from common.utils.models import UUIDModel


class Event(UUIDModel):
    title = models.CharField(max_length=255)
    start_timestamp = models.DateTimeField()
    end_timestamp = models.DateTimeField()
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    description = models.TextField(blank=True, default='')
    location = models.CharField(max_length=255, blank=True, default='')
    url = models.URLField(blank=True, null=True)
