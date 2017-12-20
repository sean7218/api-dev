from kb_blocks.blocks import Block


class Index(Block):
    TEMPLATE = "index/index.html"
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
        {
            "title": "Form Blocks",
            "state": "content=form_blocks",
            },
        {
            "title": "Authentication",
            "state": "content=auth_blocks",
            },
        {
            "title": "Models",
            "state": "content=model_blocks",
            },
        {
            "title": "Listeners",
            "state": "content=listener_blocks",
            },
        ]

    def get(self,state,data):
        context = {
            "index_links": self.INDEX_LINKS,
            }
        return context
