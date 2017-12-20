from .block import Block


class BareBlock(Block):
    """
    Subclass of block that renders no javascript or container
    """

    def renderContainer(self,content):
        return content

    def renderScript(self,state,content):
        return content
