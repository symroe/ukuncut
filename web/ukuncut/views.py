from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from django.contrib.gis.geos import Point

from ukuncut.models import Dodger, Brand


def example(request):
    location = Point(52.3, 1.2)
    closest = Dodger.objects.filter(location__dwithin=(location, 20)).distance(location).order_by('distance')[:5]
    print closest