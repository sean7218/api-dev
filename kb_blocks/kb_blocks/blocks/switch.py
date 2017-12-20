from .block import Block


class Switch(Block):
    TEMPLATE = "kb_blocks/switch.html"
    VARIABLE = None
    DEFAULT_BLOCK = None

    SCROLL_PAGE = "page"
    SCROLL_BLOCK = "block"
    SCROLL_RESET = SCROLL_PAGE

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        if self.DEFAULT_BLOCK is None:
            children = self.getChildren()
            if not children:
                raise Exception("{0} does not define any children".format(self.getName()))
            self.DEFAULT_BLOCK = children[0]

        if self.VARIABLE is None:
            self.VARIABLE = self.getName()
        self.addListener(self.VARIABLE)

        self.child_dict = self.getChildDict()

    def getChildDict(self):
        child_dict = {}
        for child in self.getChildren():
            child_instance = self.initBlock(child)
            child_dict[child_instance.getName()] = child
        return child_dict

    def get(self,state,data):
        content_name = self.getContentName(state)

        child = self.child_dict.get(content_name)
        if child is None:
            raise self.ArgumentException("child, '{0}' not found in switch, '{1}'".format(content_name,
                                                                                          self.getName()))

        content = self.renderBlock(child,state,data)

        context = {
            "content": content,
            "content_name": content_name,
            }
        return context

    def getContentName(self,state):
        content_name = state.get(self.VARIABLE)
        if content_name is None:
            default_block = self.initBlock(self.DEFAULT_BLOCK)
            content_name = default_block.getName()
        return content_name
