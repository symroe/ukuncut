# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

import views

urlpatterns = patterns('',
   url(r'^example/$',views.example, name="example"),
   url(r'^get_results/(?P<lat>.*)/(?P<lng>.*)/$',views.get_results, name="get_results"),
   url(r'^$',views.index, name="index"),
   )
