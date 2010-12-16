import urllib2
import re
import json

import BeautifulSoup
from django.contrib.gis.geos import Point

from ukuncut.models import Brand, Dodger
from openingtimes.models import OpenTime

BASE_URL = "http://www.bhs.co.uk/mall/infopageviewer.cfm/bhsstore/storelocatorbranch?branch_id="

company_id = Dodger.C_BHS
brand_name = Dodger.COMPANIES[company_id-1][1]
brand_id = company_id

try:
    brand = Brand.objects.get(brand_id=brand_id)
except Brand.DoesNotExist:
    brand = Brand(brand_id=brand_id, name=brand_name)
    brand.save()


def populate_ids():
    import redis
    r = redis.Redis(db=4)
    
    start_id = 0
    while start_id < 1000:
        req = urllib2.urlopen("%s%s" % (BASE_URL,start_id))
        soup = BeautifulSoup.BeautifulSoup(req)
        
        if not soup.findAll('img', {'src': re.compile('/mall/errors/fault.gif')}):
            print start_id
            r.sadd('bhs_ids', start_id)
        
        start_id = start_id + 1
    s = r.smembers('bhs_ids')
    print s

def parse_store(store_id, req):
    soup = BeautifulSoup.BeautifulSoup(req)
    soup = BeautifulSoup.BeautifulSoup(soup.prettify())
    soup = soup.find('div', id='MainInfo')

    name = soup.find('span', id='infoTitle').string.strip()


    address = soup.find('div', id='address').findAll('p')
    phone = address[1].find('span', {'class' : 'highlight_text'}).string.strip()

    addresses = ''.join(["%s\n" % e.strip() for e in address[0].recursiveChildGenerator() if isinstance(e,unicode)])
    addresses = addresses.strip().split('\n')
    postcode = addresses.pop(-1)

    addresses_dict = {}
    for i, address in enumerate(addresses[1:]):
        i = i+1
        addresses_dict["address%s" % i] = address

    try:
        d = Dodger.objects.get(name=name, company=company_id, postcode=postcode)
    except Exception, e:
        d = Dodger(name=name, company=company_id, postcode=postcode)
    
    d.address1 = addresses_dict.get('address1')
    d.address2 = addresses_dict.get('address2')
    d.address3 = addresses_dict.get('address3')
    d.address4 = addresses_dict.get('address4')
    d.country = "United Kingdom"
    d.brand = brand
    d.dodger_id = store_id
    
    try:
        import urllib
        args = {'address' : "%s %s" % (addresses_dict['address1'], postcode)}
        arg = urllib.urlencode(args)
        geo_url = 'http://maps.googleapis.com/maps/api/geocode/json?%s&region=gb&sensor=false' % arg
        geo_data = json.loads(urllib2.urlopen(geo_url).read())
        geo_result = geo_data['results'][0]['geometry']['location']
        print geo_result, geo_url
        d.location = Point(float(geo_result['lat']), float(geo_result['lng']))
    except Exception, e:
        print e
        print geo_url
        # raise
    try:    
        d.save()
    except Exception, e:
        print e

def scrape():
    # uncomment to ge new IDs
    # populate_ids()
    
    # known IDs
    stores = ['0', '669', '668', '667', '666', '665', '664', '663', '662', '661', '660', '578', '692', '693', '690', '691', '696', '697', '694', '695', '698', '699', '542', '543', '540', '541', '546', '547', '544', '545', '548', '549', '571', '570', '678', '679', '674', '675', '676', '677', '670', '671', '672', '710', '537', '536', '535', '534', '533', '532', '531', '530', '539', '538', '591', '590', '593', '592', '595', '594', '597', '596', '599', '598', '706', '707', '700', '701', '702', '703', '569', '526', '527', '528', '529', '586', '587', '584', '585', '582', '583', '580', '581', '588', '589', '641', '640', '643', '642', '645', '644', '647', '646', '649', '648', '673', '623', '622', '579', '620', '627', '626', '625', '624', '573', '572', '629', '628', '577', '576', '575', '574', '708', '600', '657', '704', '654', '655', '653', '650', '651', '659', '630', '631', '632', '633', '634', '635', '636', '637', '638', '639', '562', '563', '564', '565', '566', '550', '709', '551', '605', '568', '606', '559', '558', '603', '602', '555', '554', '557', '556', '609', '608', '553', '560', '561', '618', '619', '612', '613', '610', '611', '616', '617', '614', '615', '567', '689', '688', '685', '684', '687', '686', '681', '680', '683', '682']
    # stores = ['0',]
    
    for store in stores:
        req = urllib2.urlopen("%s%s" % (BASE_URL, store))
        parse_store(store, req)