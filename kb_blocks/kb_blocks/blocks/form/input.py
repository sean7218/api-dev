from .entry import Entry


class Input(Entry):
    TAG = "input"
    TYPE = "text"

    def getAttributes(self,state,data):
        attrs = super().getAttributes(state,data)
        attrs["type"] = self.TYPE
        return attrs
