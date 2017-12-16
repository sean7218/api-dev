from django.shortcuts import render
from django.http import HttpResponse
from .models import Vendor

# Create your views here.
def index(request):
    return HttpResponse("Hello, World. You're at the UberEats index.")

def vendor_create(request):
    vendors = Vendor.objects.all()
    output = ', '.join([v.name for v in vendors])
    return render(request, 'uberEats/create-vendor.html')

def vendor_read(request):
    vendors = Vendor.objects.all()
    context = { 'vendors': vendors }
    return render(request, 'uberEats/index.html', context)

def vendor_update(request):
    vendor = Vendors.objects.get(name="TN Taco Company")
    vendor.name = "Tennesse Taco Company"
    vendor.save()
    return HttpResonse(vendor.name)




