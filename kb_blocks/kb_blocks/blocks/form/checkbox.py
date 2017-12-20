from .input import Input


class Checkbox(Input):
    TYPE = "checkbox"
    CLASS = ""
    TRUE_VALUES = [
        "on",
        "true",
        True,
        "True",
        ]

    def getTitle(self,state,data):
        return None

    def getEntryContent(self,state,data):
        return super().getTitle(state,data)

    def getValue(self,state,data):
        value = super().getValue(state,data)
        if value in self.TRUE_VALUES:
            return True
        else:
            return False

    def getAttributes(self,state,data):
        attributes = super().getAttributes(state,data)
        if self.getChecked(state,data):
            attributes["checked"] = "1"
        attributes.pop("value",None)
        return attributes

    def getChecked(self,state,data):
        return bool(self.getValue(state,data))
