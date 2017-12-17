from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django import forms

# Create your views here.

def index(request):
    return HttpResponse("stacker index welcome you")

def hello(request):
    return HttpResponse("hello, stacker")

def home(request):
    context = {'name': 'sean'}
    return render(request, 'stacker/index.html', context)

class ContactView(View):
    def get(self, request):
        # <view logic>
        return render(request, 'contact.html', {'name': 'sean'})







