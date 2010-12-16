import datetime

from django.contrib.gis.db import models
from django.contrib.contenttypes import generic

from openingtimes.models import OpenTime

class Brand(models.Model):
    brand_id = models.CharField(blank=True, max_length=100, primary_key=True)
    name = models.CharField(blank=True, null=True, max_length=255)
    url = models.URLField(blank=True, verify_exists=False)


class OpenNowManager(models.GeoManager):
    def get_query_set(self):
        now = datetime.datetime.now()
        t = now.strftime('%H:%M')
        d = now.weekday()
        
        qs = super(OpenNowManager, self).get_query_set()
        return qs
        qs = qs.filter(
            opening_times__open_time__lt=t, 
            opening_times__close_time__gt=t,
            opening_times__day_of_week=d,
            )
        return qs


class Dodger(models.Model):
    
    C_ARCADIA = 1
    C_VODAFONE = 2
    C_BHS = 3
    
    COMPANIES = (
        (C_ARCADIA, 'Arcadia'),
        (C_VODAFONE, 'Vodafone'),
        (C_BHS, 'BHS'),
    )
    
    name = models.CharField(blank=True, max_length=255)
    company = models.IntegerField(blank=True, null=False, choices=COMPANIES)
    brand = models.ForeignKey(Brand, null=True)
    doger_id = models.CharField(blank=True, max_length=100)
    address1 = models.CharField(blank=True, null=True, max_length=255)
    address2 = models.CharField(blank=True, null=True, max_length=255)
    address3 = models.CharField(blank=True, null=True, max_length=255)
    address4 = models.CharField(blank=True, null=True, max_length=255)
    postcode = models.CharField(blank=True, null=True, max_length=20)
    phone = models.CharField(blank=True, null=True, max_length=100)
    location = models.PointField(spatial_index=True, geography=True, null=True, blank=True)
    country = models.CharField(blank=True, null=True, max_length=100)
    opening_times = generic.GenericRelation(OpenTime)

    objects = models.GeoManager()
    open_now = OpenNowManager()
    
    def __unicode__(self):
        return "%s - %s" % (self.name, self.brand.name)

    def is_open(self):
        return bool(self.opening_times.open_now())

class EventManager(models.GeoManager):

    def get_query_set(self):
        yesterday = datetime.datetime.today() - datetime.timedelta(1)
        qs = super(EventManager, self).get_query_set()
        return qs.filter(date__gt=yesterday)
    
    
class Event(models.Model):
    name = models.CharField(blank=True, max_length=255)
    location = models.PointField(spatial_index=True, geography=True, null=True, blank=True)
    date = models.DateField(default=datetime.datetime.today)
    url = models.URLField(blank=True, verify_exists=True)
    
    objects = EventManager()
    
    def __unicode__(self):
        return "%s, %s" % (self.name, self.date)
    