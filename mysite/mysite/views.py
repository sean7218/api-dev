from django.http import HttpResponse
from django.shortcuts import redirect
def hello_world(request):
    return HttpResponse('Hello World, from Mysite \n')

def index(request):
    return redirect('/kblock/')
