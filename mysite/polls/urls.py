from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.vendor_list, name='index'),
   #  url(r'^vendor/$', views.vendor_list, name='vendor_list'),

]
