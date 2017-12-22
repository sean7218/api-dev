
from kb_blocks.blocks import Block

class HomeBlock(Block):
    TEMPLATE = "home_block/home.html"
    AUTH = False
    HEADING = "Home Context Block"
    MESSAGE = "Home Context Block changes." \
              "Notice the state in the URL change. " \
              "Notice that these are blocks that we have seen before. "
    STATE_CHANGE = "switch_blocks=home_block"
    LINK_TEXT = "Check out Render Block"

    def get(self, state, data):
        random_number = 12
        context = {
            "heading": self.HEADING,
            "message": self.MESSAGE,
            "state_change": self.STATE_CHANGE,
            "link_text": self.LINK_TEXT,
            "random_number": random_number,
        }
        return context
