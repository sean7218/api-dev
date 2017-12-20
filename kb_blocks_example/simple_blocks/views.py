from kb_blocks.blocks import Block, Switch

import random

class SimpleBlock(Block):
    TEMPLATE = "simple_blocks/simple_block.html"
    AUTH = False


class ContextBlock(Block):
    TEMPLATE = "simple_blocks/context_block.html"
    AUTH = False
    HEADING = "Context Block"
    MESSAGE = "This is the same as the Simple Block, except that there is data passed into the template via the `context` object. The heading and this message are defined in Python within the views.py. Also, a random number is passed into the context. Most blocks operate this way, returning a dictionary as a context, with the keys and values made available in the tamplate."
    STATE_CHANGE = "simple_blocks=render_block"
    LINK_TEXT = "Check out Render Block"

    def get(self,state,data):
        random_number = random.random()
        context = {
            "heading": self.HEADING,
            "message": self.MESSAGE,
            "state_change": self.STATE_CHANGE,
            "link_text": self.LINK_TEXT,
            "random_number": random_number,
            }
        return context


class RenderBlock(Block):
    TEMPLATE = "simple_blocks/render_block.html"
    AUTH = False
    HEADING = "Render Block"
    MESSAGE = "This block is just like the Context Block, but in addition to passing simple text into the context, there is also a child-block passed in. Blocks are able to render other blocks, without having to worry what that block is doing. We can see that we are rendering a `SimpleBlock` below."
    STATE_CHANGE = "simple_blocks=render_many_blocks"
    LINK_TEXT = "Check out Render Many Blocks"
    RENDERED_BLOCK = SimpleBlock
    CHILDREN = [
        RENDERED_BLOCK,
        ]

    def get(self,state,data):
        rendered_block = self.renderBlock(self.RENDERED_BLOCK,state,data)
        context = {
            "heading": self.HEADING,
            "message": self.MESSAGE,
            "state_change": self.STATE_CHANGE,
            "link_text": self.LINK_TEXT,
            "rendered_block": rendered_block,
            }
        return context


class RenderManyBlocks(Block):
    TEMPLATE = "simple_blocks/render_many_blocks.html"
    AUTH = False
    HEADING = "Render Many Blocks"
    MESSAGE = "This block does the same thing as RenderBlock, except that it renders a list of the same block, and displays them in the template. In this case, we are using ContextBlock"
    STATE_CHANGE = "content=switch_blocks"
    LINK_TEXT = "Next section: Switch Blocks"
    RENDERED_BLOCK = ContextBlock
    RENDERED_BLOCK_COUNT = 3
    CHILDREN = [
        RENDERED_BLOCK,
        ]

    def get(self,state,data):
        rendered_block_list = []
        for i in range(self.RENDERED_BLOCK_COUNT):
            rendered_block = self.renderBlock(self.RENDERED_BLOCK,state,data)
            rendered_block_list.append(rendered_block)
        context = {
            "heading": self.HEADING,
            "message": self.MESSAGE,
            "state_change": self.STATE_CHANGE,
            "link_text": self.LINK_TEXT,
            "rendered_block_list": rendered_block_list,
            }
        return context


class SimpleBlocks(Switch):
    CHILDREN = [
        SimpleBlock,
        ContextBlock,
        RenderBlock,
        RenderManyBlocks,
        ]
    AUTH = False
