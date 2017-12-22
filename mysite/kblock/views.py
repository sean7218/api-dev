from django.shortcuts import render
from django.http import HttpResponse
from kb_blocks.blocks import Page, Content

from kblock.menu_block.views import MenuBlock

# Create your views here.
def index(request):
    return HttpResponse("Hello, world. Kblock app")




# main/views.py
class Content(Content):
    CHILDREN = [
        MenuBlock
    ]


class Main(Page):
    CONTENT_BLOCK = Content
