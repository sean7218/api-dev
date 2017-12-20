from .block import Block
from .bare_block import BareBlock
from .robots_txt import RobotsTxt
from ..common.random import getRandom

import json


class Page(BareBlock):
    TEMPLATE = "kb_blocks/page.html"
    FAVICON = "kb_blocks/img/blocks.png"
    AUTH = False
    JQUERY_JS = "https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"
    PAGE_JS = "kb_blocks/js/page.js"
    MAIN_CSS = "https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css"
    MAIN_JS = "https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"
    ERROR_MODAL_TEMPLATE = "kb_blocks/page_error_modal.html"
    ROBOTS_TXT_BLOCK = RobotsTxt
    CONTENT_BLOCK = None
    ADMIN = False
    TRACKERS = []
    CACHE_BUSTER = getRandom()

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        #Add children
        if self.CONTENT_BLOCK is None:
            raise Exception("{0} does not define self.CONTENT_BLOCK".format(self.getFullName()))
        self.addChild(self.CONTENT_BLOCK)
        self.addChild(self.ROBOTS_TXT_BLOCK)

    def get(self,state,data):
        #Initial state
        initial_state = self.makeTemplateSafe(json.dumps(state))

        #Render the content block
        try:
            content = self.renderBlock(self.CONTENT_BLOCK,state,data)
        except (self.UserException,
                self.ArgumentException,
                self.NotFoundException,
                self.NotAuthenticatedException) as e:
            raise Exception(e)

        #Get the CSS and JS lists
        css_list = self.getCssList()
        js_list = self.getJsList()

        #Trackers for analytics
        kb_blocks_tracker = {
            "id": "UA-89983744-1",
            "name": "kb_blocks_tracker",
            }
        trackers = [kb_blocks_tracker] + self.TRACKERS
        trackers = self.makeTemplateSafe(json.dumps(trackers))

        static_prefix = self.getStaticUrl()

        context = {
            "initial_state": initial_state,
            "content": content,
            "css_list": css_list,
            "js_list": js_list,
            "tracker_list": trackers,
            "static_prefix": static_prefix,
            }
            
        return context

    def getCssList(self):
        css_list = super().getCssList()
        css_list = [self.MAIN_CSS] + css_list
        css_list = self.getUniqueList(css_list)
        return css_list

    def getJsList(self):
        js_list = super().getJsList()
        page_js = self.getPageJs()
        js_list = [self.JQUERY_JS,page_js,self.MAIN_JS] + js_list
        js_list = self.getUniqueList(js_list)
        return js_list

    def getPageJs(self):
        if self.getDebug():
            cache_buster = self.getRandom()
        else:
            cache_buster = self.CACHE_BUSTER
        return "{0}?{1}".format(self.PAGE_JS,cache_buster)

    def getRoutes(self):
        routes = super().getRoutes()

        root_view = self.getView(self.CONTENT_TYPE_HTML,None)
        root_route = self.getRoute("$",root_view)
        routes = [root_route] + routes

        #Get the media route for development
        debug = self.getDebug()
        media_root = self.getMediaRoot()
        media_url = self.getMediaUrl()
        if debug and media_root and media_url:
            media_url = media_url.lstrip("/")
            media_route = self.getRoute("{0}(?P<path>.*)$".format(media_url),
                                        self.getMediaView(),
                                        document_root=media_root)
            routes += [media_route]

        #Admin console
        if self.ADMIN:
            admin_url = self.getAdminUrl()
            if not admin_url:
                admin_url = "/admin/"
            admin_url = admin_url.lstrip("/")
            admin_route = self.getRoute(admin_url,self.getAdminView())
            routes += [admin_route]

        return routes

    def getRandom(self):
        return getRandom()
