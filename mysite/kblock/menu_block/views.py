
from kblock.dashboard_block.views import DashboardBlock
from kblock.home_block.views import HomeBlock
from kblock.profile_block.views import ProfileBlock

from kb_blocks.blocks import Block, Switch

# all the switch blocks were encapsulated here as SPA tabs i.e. the main menu
class MenuBlock(Switch):
    TEMPLATE = "menu_block/menu.html"
    AUTH = False
    HEADING = "Menu"
    MESSAGE = "Below is SPA menu and please select the menu item you want"
    CHILDREN = [
        HomeBlock,
        DashboardBlock,
        ProfileBlock,
    ]

    def get(self, state, data):
        children = []
        for child in self.getChildren():
            c = self.initBlock(child)
            c.name = c.getName()
            children.append(c)

        context = {
            "heading": self.HEADING,
            "message": self.MESSAGE,
            "children": children,
        }
        switch_context = super().get(state, data)
        context.update(switch_context)
        return context
