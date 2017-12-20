from .bare_block import BareBlock


class RobotsTxt(BareBlock):
    TEMPLATE = "kb_blocks/robots.txt"
    AUTH = False
    ROBOTS_PATH = "robots.txt"

    def getRoutes(self):
        routes = super().getRoutes()
        robots_view = self.getView(self.CONTENT_TYPE_HTML,None)
        robots_route = self.getRoute(self.ROBOTS_PATH,robots_view)
        routes.append(robots_route)
        return routes
