import re
import urllib2
import urllib
import urlparse
import cookielib
import BeautifulSoup

from django.contrib.gis.geos import Point

from ukuncut.models import Dodger, Brand
from openingtimes.models import OpenTime

cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
urllib2.install_opener(opener)
urlopen = urllib2.urlopen
Request = urllib2.Request
headers = {'User-Agent' : "Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11"}

company_id = Dodger.C_VODAFONE
brand_id = company_id

brand_name = Dodger.COMPANIES[company_id-1][1]
print brand_name

try:
    brand = Brand.objects.get(brand_id=brand_id)
except Brand.DoesNotExist:
    brand = Brand(brand_id=brand_id, name=brand_name)
    brand.save()


def make_grid():
    UK_BOUNDS = {
        'NORTH': 61.0, 
        'SOUTH': 49.0, # Includes Jersey
        'EAST': 1.8,
        'WEST': -8.2,
    }
    

    
    def float_range(start, end, step_range=1.47):
        """
        1.47 is *roughly* 100 miles
        """
        STEPS = []
        while start < end:
            STEPS.append(start)
            start = start + step_range
        return STEPS
         
    X_STEPS = float_range(UK_BOUNDS['SOUTH'], UK_BOUNDS['NORTH'], step_range=5.0)
    Y_STEPS = float_range(UK_BOUNDS['WEST'], UK_BOUNDS['EAST'], step_range=5.0)
    
    grid = []
    for x_step in X_STEPS:
        row = []
        for y_step in Y_STEPS:
            row.append((x_step,y_step))
        grid.append(row)
    return grid

def bootstrap():
    # Insane bootstrapping
    print brand_name, "boot strapping"
    initial_url1 = "http://www.vodafone.co.uk/personal/index.htm"
    initial_url2 = "http://online.vodafone.co.uk/dispatch/Portal/appmanager/vodafone/wrp?_nfpb=true&_pageLabel=Page_Help_StoreLocator&pageID=SL_0001"
    initial_url3 = "http://online.vodafone.co.uk/dispatch/Portal/appmanager/vodafone/wrp?_nfpb=true&Portlet_BOS_StoreLocator_Page_Help_StoreLocator_actionOverride=/portlets/ecare/storelocator/browse&_windowLabel=Portlet_BOS_StoreLocator_Page_Help_StoreLocator&_pageLabel=Page_Help_StoreLocator"

    req = Request(initial_url1, headers=headers)
    handle = urlopen(req) 
    print brand_name, "Loaded home page"
    req = Request(initial_url2, headers=headers)
    handle = urlopen(req) 
    print brand_name, "Loaded form page"

    post_data = urllib.urlencode(
        {
            'action': 'places.cgi',
            'client': 'vodafone_unity',
            'count': '5',
            'filter': 'All',
            'db': 'hcgaz',
            'place': '',
            'f_county': 'Aberdeenshire',
            'x': '27',
            'y': '4',
        }
        )
    
    req = Request(initial_url3, post_data, headers=headers)
    handle = urlopen(req) 
    print brand_name, "Posted Form"


    # End Bootstrap.  Yes, all 3 requests are needed.
    print brand_name, "Ended bootstrap"


def parse(handle):
    # req = urllib2.urlopen(url)
    soup = BeautifulSoup.BeautifulSoup(handle)
    result_div = soup.find('div', {'class' : 'tableTopBorder'})
    for result in result_div.findAll('tr', {'class' : re.compile('lightBlue')}):
        try:
            cells = result.findAll('td')

            addresses = ''.join([e for e in cells[1].recursiveChildGenerator() if isinstance(e,unicode)])
            addresses = addresses.strip().split('\n')

            name = addresses.pop(0)
            postcode = addresses.pop(-1)

            addresses_dict = {}
            for i, address in enumerate(addresses):
                i = i+1
                addresses_dict["address%s" % i] = address

            url = cells[-1].a['href']
            parsed_url = urlparse.parse_qs(url)
            lat = parsed_url['lat']
            lon = parsed_url['lon']

            try:
                d = Dodger.objects.get(name=name, company=company_id, postcode=postcode)
            except Exception, e:
                d = Dodger(name=name, company=company_id, postcode=postcode)

            d.address1 = addresses_dict.get('address1')
            d.address2 = addresses_dict.get('address2')
            d.address3 = addresses_dict.get('address3')
            d.address4 = addresses_dict.get('address4')
            d.country = "United Kingdom"
            d.location = Point(float(lat[0]), float(lon[0]))
            d.brand = brand
            d.save()
        except Exception, e:
            print brand_name, e

def parse_details(handle):
    soup = BeautifulSoup.BeautifulSoup(handle)
    result_div = soup.find('div', {'id' : 'template9_middle_bottom_left'})
    for result in result_div.findAll('div', {'class' : re.compile('transBack')}):
        try:
            cells = result.findAll('p', {'class' : 'paddingTop10'})

            addresses = ''.join([e for e in cells[3].recursiveChildGenerator() if isinstance(e,unicode)])
            addresses = addresses.strip().split('\n')

            name = addresses.pop(0)
            postcode = addresses.pop(-1)

            addresses_dict = {}
            for i, address in enumerate(addresses):
                i = i+1
                addresses_dict["address%s" % i] = address

            phone = cells[2].contents[1].split(' or ')[0].strip()

            try:
                d = Dodger.objects.get(name=name, company=company_id, postcode=postcode)
            except Exception, e:
                d = Dodger(name=name, company=company_id, postcode=postcode)
                print "unknown store"
            
            d.phone = phone
            d.save()

            opening_times = cells[1]
            if len(opening_times) > 3:
                # print opening_times
                opening_times = ''.join([e for e in opening_times.recursiveChildGenerator() if isinstance(e,unicode)])
                opening_times = opening_times.split('\n')[2:]

                mon = opening_times[0]
                tue = opening_times[1]
                wed = opening_times[2]
                thu = opening_times[3]
                fri = opening_times[4]
                sat = opening_times[5]
                sun = opening_times[6]

            # Delete all opeing times for this Dodger
            d.opening_times.all().delete()
            def parse_open_time(str_time):
                # Sunday: 1000-1630
                if str_time:
                    open_close = str_time.split(':')[1]
                    open_close = open_close.split('-')
                    if len(open_close) >= 2:
                        for i,v in enumerate(open_close):
                            v = v.replace('.', ':').strip()
                            v = list(v)
                            v.insert(2, ':')
                            v = "".join(v)
                            open_close[i] = v
                        return open_close
            try:
                # Monday
                open_close = parse_open_time(mon)
                if mon and open_close:
                    o = d.opening_times.create(day_of_week=0, open_time=open_close[0], close_time=open_close[1])
                # Tuesday
                open_close = parse_open_time(tue)
                if tue and open_close:
                    o = d.opening_times.create(day_of_week=1, open_time=open_close[0], close_time=open_close[1])
                # Wednesday
                open_close = parse_open_time(wed)
                if wed and open_close:
                    o = d.opening_times.create(day_of_week=2, open_time=open_close[0], close_time=open_close[1])
                # Thursday
                open_close = parse_open_time(thu)
                if thu and open_close:
                    o = d.opening_times.create(day_of_week=3, open_time=open_close[0], close_time=open_close[1])
                # Friday
                open_close = parse_open_time(fri)
                if fri and open_close:
                    o = d.opening_times.create(day_of_week=4, open_time=open_close[0], close_time=open_close[1])
                # Saturday
                open_close = parse_open_time(sat)
                if sat and open_close:
                    o = d.opening_times.create(day_of_week=5, open_time=open_close[0], close_time=open_close[1])
                # Sunday
                open_close = parse_open_time(sun)
                if sun and open_close:
                    o = d.opening_times.create(day_of_week=6, open_time=open_close[0], close_time=open_close[1])
            except Exception, e:
                print "error parsing opening times"
                print e
                print open_close

        except Exception, e:
            print brand_name, e



def scrape():
    """
    Grab all the data from the vodafone store finder page.
    
    They allow distance lookups, but wont give more than 149 results per page,
    so we need to get the bounds of the UK and 'page' over it, guessing how far
    we need to step each time.  100 miles seems alright for the time being.
    """
    
    grid = make_grid()
    
    bootstrap()
        
    for row in grid:
        for cell in row:
            url = "http://online.vodafone.co.uk/dispatch/Portal/appmanager/vodafone/wrp?_nfpb=true&Portlet_BOS_StoreLocator_Page_Help_StoreLocator_actionOverride=/portlets/ecare/storelocator/browse&_windowLabel=Portlet_BOS_StoreLocator_Page_Help_StoreLocator&_pageLabel=Page_Help_StoreLocator&action=http://www.multimap.com/clients/browse.cgi&client=vodafone_unity&lon=%s&lat=%s&scale=10000&width=460&height=300&rt=browse&count=149&filter=All&coordsys=gb" % cell
            req = Request(url, headers=headers)
            handle = urlopen(req) 
            parse(handle)

            url = "http://online.vodafone.co.uk/dispatch/Portal/appmanager/vodafone/wrp?_nfpb=true&Portlet_BOS_StoreLocator_Page_Help_StoreLocator_actionOverride=/portlets/ecare/storelocator/browse&_windowLabel=Portlet_BOS_StoreLocator_Page_Help_StoreLocator&_pageLabel=Page_Help_StoreLocator&action=http://www.multimap.com/clients/browse.cgi&client=vodafone_unity&lon=%s&lat=%s&scale=10000&width=460&height=300&rt=browse2&count=149&filter=All&coordsys=gb" % cell
            req = Request(url, headers=headers)
            handle = urlopen(req) 
            parse_details(handle)
