from django.contrib.gis.db import models

class Brand(models.Model):
    brand_id = models.CharField(blank=True, max_length=100, primary_key=True)
    name = models.CharField(blank=True, null=True, max_length=255)
    url = models.URLField(blank=True, verify_exists=False)


class Dodger(models.Model):
    
    C_ARCADIA = 1
    C_VODAFONE = 2
    
    COMPANIES = (
        (C_ARCADIA, 'Arcadia'),
        (C_VODAFONE, 'Vodafone'),
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
    location = models.PointField(spatial_index=True, null=True, blank=True)
    country = models.CharField(blank=True, null=True, max_length=100)

    objects = models.GeoManager()
    
    def __unicode__(self):
        return "%s - %s" % (self.name, self.brand.name)