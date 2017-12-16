from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$',views.index, name='index'),
    url(r'^vendor/create$', views.vendor_create, name='vendor_create'),
    url(r'^vendor/read$', views.vendor_read, name='vendor_read'),
    ]




