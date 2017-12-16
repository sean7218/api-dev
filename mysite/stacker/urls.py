from django.conf.urls import url

from . import views

urlpatterns = [
        # /stacker/
        url(r'^$', views.index, name='index'),
        # /stacker/hello
        url(r'^hello$', views.hello, name='hello'),
        # /stacker/home
        url(r'^home$', views.home, name='home'),

]
