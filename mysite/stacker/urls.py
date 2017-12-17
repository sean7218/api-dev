from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
        # /stacker/
        url(r'^$', views.index, name='index'),
        # /stacker/hello
        url(r'^hello$', views.hello, name='hello'),
        # /stacker/home
        url(r'^home$', views.home, name='home'),
        # /stacker/contact
        path('contact', views.ContactView.as_view(), name='contact'),


]
