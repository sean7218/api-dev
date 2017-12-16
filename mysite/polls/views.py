from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello World \n")

def vendor_list(request):
    return render(request, 'polls/vendor_list.html')



# Create your views here.
