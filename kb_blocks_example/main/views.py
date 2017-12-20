from kb_blocks.blocks import Page, Content, Block
from index.views import Index
from simple_blocks.views import SimpleBlocks
from switch_blocks.views import SwitchBlocks
from form_blocks.views import FormBlocks
from auth_blocks.views import AuthBlocks, NeedsLogin
from model_blocks.views import ModelBlocks
from listener_blocks.views import ListenerBlocks


class Content(Content):
    CHILDREN = [
        Index,
        SimpleBlocks,
        SwitchBlocks,
        FormBlocks,
        AuthBlocks,
        NeedsLogin,
        ModelBlocks,
        ListenerBlocks,
        ]
    AUTH_BLOCK = AuthBlocks

class Main(Page):
    CONTENT_BLOCK = Content
