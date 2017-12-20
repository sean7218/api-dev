from .block import Block


class NotFound(Block):
    TEMPLATE = "kb_blocks/not_found.html"
    AUTH = False
