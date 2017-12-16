from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    return HttpResponse("stacker index welcome you")

def hello(request):
    return HttpResponse("hello, stacker")

def home(request):
    context = {'name': 'sean'}
    return render(request, 'stacker/index.html', context)
