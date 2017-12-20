from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django import forms
from django.views.generic.edit import (CreateView, UpdateView, FormView)
from stacker.models import Stack


# Create your views here.

def index(request):
    context = {'title': 'home' }
    return render(request, 'stacker/index.html', context)

def hello(request):
    return HttpResponse("hello, stacker")

def home(request):
    context = {'name': 'sean', 'title':'home'}
    return render(request, 'stacker/index.html', context)

class ContactView(View):
    def get(self, request):
        # <view logic>
        context = {'title': 'contact'}
        return render(request, 'stacker/contact.html', context)

class BlogView(View):
    def get(self, request):
        # <view logic>
        context = {'title': 'blog'}
        return render(request, 'stacker/blog.html', context)

class CreateStackView(CreateView):
    model = Stack
    fields = ['name', 'category', 'goal', 'balance','owner']
    template_name = 'stacker/stack_create_form.html'

class UpdateStackView(UpdateView):
    model = Stack
    fields = ['name', 'category', 'goal', 'balance','owner']
    template_name_suffix = '_update_form'












