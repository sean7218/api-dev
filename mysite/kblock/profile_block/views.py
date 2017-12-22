from kb_blocks.blocks import Block

class ProfileBlock(Block):
    TEMPLATE = "profile_block/profile.html"
    AUTH = False
    HEADING = "Profile"
    MESSAGE = "This block will show the user information. " \
              "Such as the linked bank accounts, the social media connections. " \
              "This block also allow the user to logout. "


    def get(self, state, data):

        context = {
            "heading": self.HEADING,
            "message": self.MESSAGE,
        }
        return context
