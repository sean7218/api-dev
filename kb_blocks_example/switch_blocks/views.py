from kb_blocks.blocks import Block, Switch
from simple_blocks.views import SimpleBlock, ContextBlock,\
                                RenderBlock, RenderManyBlocks


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


class SwitchExample(Switch):
    TEMPLATE = "switch_blocks/switch_example.html"
    AUTH = False
    HEADING = "Switch Block Example"
    MESSAGE = "Click on any of the links below to see how the content changes. Notice the state in the URL change. Notice that these are blocks that we have seen before."
    STATE_CHANGE = "content=form_blocks"
    LINK_TEXT = "Next"
    CHILDREN = [
        SimpleBlock,
        ContextBlock,
        RenderBlock,
        RenderManyBlocks,
        ]

    def get(self,state,data):
        children = []
        for child in self.getChildren():
            c = self.initBlock(child)
            c.name = c.getName()
            children.append(c)

        context = {
            "heading": self.HEADING,
            "message": self.MESSAGE,
            "state_change": self.STATE_CHANGE,
            "link_text": self.LINK_TEXT,
            "children": children,
            }
        switch_context = super().get(state,data)
        context.update(switch_context)
        return context


class SwitchBlocks(Switch):
    CHILDREN = [
        SwitchIntro,
        SwitchExample,
        ]
    AUTH = False
