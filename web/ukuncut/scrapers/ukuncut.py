import urllib
import urlparse
import urllib2
import re
import datetime

import BeautifulSoup

from django.contrib.gis.geos import Point
from web.ukuncut.models import Event

def scrape():
    print "ukuncut"

    url_base = "http://www.ukuncut.org.uk"
    url = "%s/actions" % url_base
    req = urllib2.urlopen(url)
    soup = BeautifulSoup.BeautifulSoup(req)
    
    maps = soup.findAll('iframe', {'src' : re.compile(r'/actions/map')})
    
    map_urls =  ["%s%s" % (url_base, m['src']) for m in maps]


    for map_url in map_urls:
        req = urllib2.urlopen(map_url)
        page = req.read()
        soup = BeautifulSoup.BeautifulSoup(page)
        date_str = urlparse.parse_qs(map_url.split('?')[1])
        event_date =  datetime.datetime.strptime(date_str['date'][0], '%Y-%m-%d')
        
        # events = re.search(r"""google\.maps\.event\.addListener(.*);""", page, re.M)
        events = re.split(r"""var marker_""", page)
        for event in events:
            event_name_re = re.search(r"""href="/actions/([\d]+)">([^<]+)</a>""", event)
            if event_name_re:
                event_name = event_name_re.groups()[1][3:].split(',')[0]
                print event_name
                
                event_url = "%s/actions/%s" % (url_base, event_name_re.groups()[0])
                
                event_latlng = re.search(r"""new google\.maps\.LatLng\(([^,]+),([^)]+)\)""", event)
                (lat, lng) = event_latlng.groups(1)
            
                try:
                    e = Event.objects.get(name=event_name, date=event_date)
                except Event.DoesNotExist:
                    e = Event(name=event_name, date=event_date)
                e.location = Point(float(lat), float(lng))
                e.url = event_url
                e.save()