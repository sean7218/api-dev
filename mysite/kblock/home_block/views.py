
from kb_blocks.blocks import Block

class HomeBlock(Block):
    TEMPLATE = "home_block/home.html"
    AUTH = False
    HEADING = "Home"
    MESSAGE = "This SPA have three blocks. " \
              "All blocks are embedded inside the main switch block. " \
              "The main switch block is called menu_block "

    def get(self, state, data):
        context = {
            "heading": self.HEADING,
            "message": self.MESSAGE,
        }
        return context
