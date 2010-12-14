import datetime

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

class OpenTimeManager(models.Manager):

    def open_now(self):
        now = datetime.datetime.now()
        t = now.strftime('%H:%M')
        d = now.weekday()

        qs = self
        qs = qs.filter(
            open_time__lt=t, 
            close_time__gt=t,
            day_of_week=d,
            )
        return qs

class OpenTime(models.Model):
    """
    Generic model for storing opening times.
    """
    content_type = models.ForeignKey(ContentType)
    object_id = models.CharField(blank=False, null=False, max_length=100)
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    day_of_week = models.IntegerField(blank=False, null=False)
    open_time = models.TimeField(blank=True)
    close_time = models.TimeField(blank=True)
    
    objects = OpenTimeManager()