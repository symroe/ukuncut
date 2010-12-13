from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from django.contrib.gis.geos import Point

from ukuncut.models import Dodger, Brand


def example(request):
    location = Point(52.25258979999999994, 0.71627930000000000)
    closest = Dodger.open_now.filter(location__dwithin=(location, 20)).distance(location).order_by('distance')[:10]

    res = HttpResponse()
    for d in closest:
        res.write("%s<br>" % d)
    return res