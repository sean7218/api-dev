from django.shortcuts import render
from django.http import HttpResponse
from kb_blocks.blocks import Page, Content, Block, Switch



# Create your views here.
def index(request):
    return HttpResponse("Hello, world. Kblock app")

# Index/views.py
class Index(Block):
    TEMPLATE = 'index/index.html'
    AUTH = False
    INDEX_LINKS = [
        {
            "title": "Simple Blocks",
            "state": "content=simple_blocks",
            },
        {
            "title": "Switch Blocks",
            "state": "content=switch_blocks",
            },

        ]

    def get(self, state, data):
        context = {
                "index_links": self.INDEX_LINKS,
                }
        return context

# SimpleBlocks/views.py
class SimpleBlock(Block):
    TEMPLATE = "simple_blocks/simple_block.html"
    AUTH = False

class SimpleBlocks(Switch):
    CHILDREN = [
        SimpleBlock
    ]
    AUTH = False

# switch_blocks/view.py
class SwitchIntro(Block):
    TEMPLATE = "switch_blocks/switch_intro.html"
    AUTH = False
    HEADING = "Switch Blocks"
    MESSAGE = "Switch Blocks are a special kind of block that has one or more child-blocks, but only renders one at a time. The block listens for a state parameter, based on its name, and will display the block that is named in that state param."
    STATE_CHANGE = "switch_blocks=switch_example"
    LINK_TEXT = "Try it"

    def get(self,state,data):
        context = {
            "heading": self.HEADING,
            "message": self.MESSAGE,
            "state_change": self.STATE_CHANGE,
            "link_text": self.LINK_TEXT,
            }
        return context

class SwitchBlocks(Switch):
    CHILDREN = [
        SwitchIntro,
        ]
    AUTH = False

# main/views.py
class Content(Content):
    CHILDREN = [
        Index,
        SimpleBlocks,
        SwitchBlocks,
    ]

class Main(Page):
    CONTENT_BLOCK = Content
