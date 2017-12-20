from ..block import Block


class FormContent(Block):
    TEMPLATE = "kb_blocks/form/form_content.html"

    def get(self,state,data):
        context = super().get(state,data)
        entries = self.getEntries(state,data)
        for entry in entries:
            context[entry.getName()] = entry
        context["entries"] = entries
        return context

    def getEntries(self,state,data):
        entries = []
        for entry in self.getChildren():
            block = self.renderBlock(entry,state,data)
            entries.append(block)
        return entries

    def getValue(self,state,data):
        """
        Some blocks are able to read a specfic value that is passed in from the data
        One example would be an entry in a form
        In those cases, a single value is returned
        Otherwise a block will return each of its children's values in a dict
        """
        val = {}
        for child in self.getChildren():
            child = self.initBlock(child)
            value = child.getValue(state,data)
            val[child.getName()] = value
        return val

    def validate(self,state,data):
        for entry in self.getChildren():
            e = self.initBlock(entry)
            e.validate(state,data)
