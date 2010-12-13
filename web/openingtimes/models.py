import datetime

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic


class OpenTime(models.Model):
    """
    Generic model for storing opening times.
    """

    content_type = models.ForeignKey(ContentType)
    object_id = models.IntegerField(blank=True, null=True)
    content_object = generic.GenericForeignKey()
    day_of_week = models.IntegerField(blank=False, null=False)
    open_time = models.TimeField(blank=True)
    close_time = models.TimeField(blank=True)
    
    objects = models.Manager()