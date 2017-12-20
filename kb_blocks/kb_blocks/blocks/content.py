from .switch import Switch
from .not_found import NotFound


class Content(Switch):
    """
    Content is the main block that is loaded into the page block
    """
    AUTH = False
    AUTH_BLOCK = None
    NOT_FOUND_BLOCK = NotFound
    EXCEPTION_VARIABLE = "exception"
    RENDER_BLOCK_VARIABLE = "render_block"
    LISTENERS = [
        "exception",
        ]

    def __init__(self,*args,**kwargs):
        if self.NOT_FOUND_BLOCK is None:
            raise Exception("{0} does not define self.NOT_FOUND_BLOCK".format(self.getName()))
        self.addChild(self.NOT_FOUND_BLOCK)
            
        self.exception_blocks = {
            self.EXCEPTION_TYPE_NOT_FOUND: self.NOT_FOUND_BLOCK
            }
        if self.AUTH_BLOCK is not None:
            self.exception_blocks[self.EXCEPTION_TYPE_NOT_AUTHENTICATED] = self.AUTH_BLOCK
            self.addChild(self.AUTH_BLOCK)

        super().__init__(*args,**kwargs)

    def get(self,state,data):
        render_block = state.get(self.RENDER_BLOCK_VARIABLE)
        if render_block is not None:
            #Render just the block that was specified
            block = self.findChild(render_block)
            if block is None:
                #Could not find the child
                raise self.NotFoundException
            self.addChild(block)

            content = self.renderBlock(block,state,data)

            context = {
                "content": content,
                }
            return context

        exception = state.pop(self.EXCEPTION_VARIABLE,None)
        if exception is not None:
            exception_block = self.exception_blocks.get(exception)
            if exception_block is None:
                raise Exception("could not handle exception {0}".format(exception))
            exception_block = self.initBlock(exception_block)
            state[self.getName()] = exception_block.getName()
            return super().get(state,data)

        
        context = None
        try:
            context = super().get(state,data)
        except self.NotAuthenticatedException:
            state[self.EXCEPTION_VARIABLE] = self.EXCEPTION_TYPE_NOT_AUTHENTICATED
        except self.NotFoundException:
            state[self.EXCEPTION_VARIABLE] = self.EXCEPTION_TYPE_NOT_FOUND
        except self.ArgumentException:
            state[self.EXCEPTION_VARIABLE] = self.EXCEPTION_TYPE_NOT_FOUND

        if context is None:
            context = self.get(state,data)

        return context

    def findChild(self,block_name):
        raise NotImplementedError
