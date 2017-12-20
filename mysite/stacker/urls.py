from django.conf.urls import url
from django.urls import path
from . import views

app_name = 'stacker'
urlpatterns = [
        # /stacker

        # /stacker/
        url(r'^$', views.index, name='index'),
        # /stacker/hello
        url(r'^hello$', views.hello, name='hello'),
        # /stacker/home
        url(r'^home$', views.home, name='home'),
        # /stacker/contact
        path('contact', views.ContactView.as_view(), name='contact'),
        # /stacker/blog
        path('blog', views.BlogView.as_view(), name='blog'),
        # /stacker/create
        path('create', views.CreateStackView.as_view(), name='create_stack'),
        # /stacker/update
        path('update/<int:pk>', views.UpdateStackView.as_view(), name='update_stack'),


]
