# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

import views

urlpatterns = patterns('',
   url(r'^example/$',views.example, name="example"),
   url(r'^get_results/(?P<lat>.*)/(?P<lng>.*)/$',views.get_results, name="get_results"),
   url(r'^get_events/(?P<lat>.*)/(?P<lng>.*)/$',views.get_events, name="get_events"),
   url(r'^$',views.index, name="index"),
   url(r'^dodgers\.kml/$',views.kml, name="kml"),
   url(r'^what$',views.instructions, name="instructions"),
   )
