from .entry import Entry


class Text(Entry):
    TAG = "textarea"
    ROWS = 3
    CONTENT_CONTAINER = False

    def get(self,state,data):
        context = super().get(state,data)
        context["attributes"].pop("value")
        return context

    def getEntryContent(self,state,data):
        return self.getValue(state,data)

    def getAttributes(self,state,data):
        attrs = super().getAttributes(state,data)
        attrs["rows"] = self.ROWS
        return attrs
