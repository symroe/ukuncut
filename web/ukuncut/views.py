from django.core import serializers

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D

from ukuncut.models import Dodger, Brand

def index(request):

    return render_to_response(
      'mobile_results.html', 
      context_instance=RequestContext(request)
    )  

def get_results(request, lat, lng):
    (lat, lng) = (float(lat), float(lng))
    location = Point(lat, lng)

    results = Dodger.objects.filter(location__dwithin=(location, D(mi=20))).distance(location).order_by('distance')[:10]
    # results = Dodger.objects.distance(location).order_by('distance')[:10]

    if request.GET.get('callback'):
        results = serializers.serialize("json", results)
        output = "%s (%s)" % (request.GET['callback'], results)
        return HttpResponse(results)
    
    your_location = (lat, lng)
    
    return render_to_response(
      'results_ahah.html', 
      {
      'results': results,
      'your_location': your_location,
      },
      context_instance=RequestContext(request)
    )  
    

def example(request):
    location = Point(52.25258979999999994, 0.71627930000000000)
    closest = Dodger.open_now.filter(location__dwithin=(location, 20)).distance(location).order_by('distance')[:10]

    res = HttpResponse()
    for d in closest:
        res.write("%s<br>" % d)
    return res


def kml(request):
    results = Dodger.objects.all()
    
    return render_to_response(
      'kml.html', 
      {
      'results': results,
      },
      context_instance=RequestContext(request)
    )  
    
    