import json
import urllib2
import re

from django.contrib.gis.geos import Point

from web.ukuncut.models import Brand, Dodger
from openingtimes.models import OpenTime

# test_url = "http://cloudservices.arcadiagroup.co.uk/storestock/storestock?brand=12556&jsonp_callback=jsonp1292077523475&lat=51.461752&long=-0.114286&dist=50000&res=10&_=1292077544710"

def scrape():
    
    company_id = Dodger.C_ARCADIA
    
    brands = ( 
        (12551,'Burton',          "http://cloudservices.arcadiagroup.co.uk/storestock/storestock?brand=12551&jsonp_callback=jsonp1292077523475&lat=51.461752&long=-0.114286&dist=50000&res=10000000&_=1292077544710",),
        (12552,'Dorothy Perkins', "http://cloudservices.arcadiagroup.co.uk/storestock/storestock?brand=12552&jsonp_callback=jsonp1292077523475&lat=51.461752&long=-0.114286&dist=50000&res=10000000&_=1292077544710",),
        (12553,'Evans',           "http://cloudservices.arcadiagroup.co.uk/storestock/storestock?brand=12553&jsonp_callback=jsonp1292077523475&lat=51.461752&long=-0.114286&dist=50000&res=10000000&_=1292077544710",),
        (12554,'Miss selfridge',  "http://cloudservices.arcadiagroup.co.uk/storestock/storestock?brand=12554&jsonp_callback=jsonp1292077523475&lat=51.461752&long=-0.114286&dist=50000&res=10000000&_=1292077544710",),
        (12555,'Topshop',         "http://cloudservices.arcadiagroup.co.uk/storestock/storestock?brand=12555&jsonp_callback=jsonp1292077523475&lat=51.461752&long=-0.114286&dist=50000&res=10000000&_=1292077544710",),
        (12556,'Topman' ,         "http://cloudservices.arcadiagroup.co.uk/storestock/storestock?brand=12556&jsonp_callback=jsonp1292077523475&lat=51.461752&long=-0.114286&dist=50000&res=10000000&_=1292077544710",),
        (12557,'Wallis',          "http://cloudservices.arcadiagroup.co.uk/storestock/storestock?brand=12557&jsonp_callback=jsonp1292077523475&lat=51.461752&long=-0.114286&dist=50000&res=10000000&_=1292077544710",),
    )

    for brand_id, brand_name, url in brands:
    
        try:
            brand = Brand.objects.get(brand_id=brand_id)
        except Brand.DoesNotExist:
            brand = Brand(brand_id=brand_id, name=brand_name)
            brand.save()
        
        r = urllib2.Request(url, headers={'User-Agent' : "Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11"})
        res = urllib2.urlopen(r)
        x = res.read()[19:-2]

        data = json.loads(x)
    
        for store in data['stores']['store']:
            for k,v in store.items():
                store[k] = v.encode('utf8')
            
            try:
                d = Dodger.objects.get(company=company_id, doger_id=store['storeId'], brand=brand)
            except Dodger.DoesNotExist:
                d = Dodger()
            d.name = store['storeName']
            d.company = company_id
            d.brand = brand
            d.doger_id = store['storeId']
            d.address1 = store.get('address1')
            d.address2 = store.get('address2')
            d.address3 = store.get('address3')
            d.address4 = store.get('address4')
            d.postcode = store.get('postcode')
            d.phone = store.get('telephoneNumber')
            # d.location = fromstr('POINT(%s, %s)' % (store['latitude'], store['longitude']))
            # d.location = 'POINT((%s, %s))' % (store['latitude'], store['longitude'])
            if float(store['latitude']) and float(store['longitude']):
                d.location = Point(float(store['latitude']), float(store['longitude']))
            d.country = store['country']
            d.save()
            
            
            # Delete all opeing times for this Dodger
            d.opening_times.all().delete()
            
            def parse_open_time(str_time):
                # 08:00-21:00
                if str_time:
                    open_close = str_time.split('-')
                    if len(open_close) >= 2:
                        open_close = [v.replace('.', ':') for v in open_close]
                        return open_close
                
            try:
                # Monday
                open_close = parse_open_time(store.get('openingMon'))
                if store.get('openingMon') and open_close:
                    o = d.opening_times.create(day_of_week=0, open_time=open_close[0], close_time=open_close[1])
                # Tuesday
                open_close = parse_open_time(store.get('openingTue'))
                if store.get('openingTue') and open_close:
                    o = d.opening_times.create(day_of_week=1, open_time=open_close[0], close_time=open_close[1])
                # Wednesday
                open_close = parse_open_time(store.get('openingWed'))
                if store.get('openingWed') and open_close:
                    o = d.opening_times.create(day_of_week=2, open_time=open_close[0], close_time=open_close[1])
                # Thursday
                open_close = parse_open_time(store.get('openingThu'))
                if store.get('openingThu') and open_close:
                    o = d.opening_times.create(day_of_week=3, open_time=open_close[0], close_time=open_close[1])
                # Friday
                open_close = parse_open_time(store.get('openingFri'))
                if store.get('openingFri') and open_close:
                    o = d.opening_times.create(day_of_week=4, open_time=open_close[0], close_time=open_close[1])
                # Saturday
                open_close = parse_open_time(store.get('openingSat'))
                if store.get('openingSat') and open_close:
                    o = d.opening_times.create(day_of_week=5, open_time=open_close[0], close_time=open_close[1])
                # Sunday
                open_close = parse_open_time(store.get('openingSun'))
                if store.get('openingSun') and open_close:
                    o = d.opening_times.create(day_of_week=6, open_time=open_close[0], close_time=open_close[1])
            except Exception, e:
                print e
                print open_close
                