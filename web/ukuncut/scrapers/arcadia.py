import json
import urllib2

from django.contrib.gis.geos import Point

from ukuncut.models import Brand, Dodger

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