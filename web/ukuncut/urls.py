# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

import views

urlpatterns = patterns('',
   url(r'^example/$',views.example, name="example"),
   )
