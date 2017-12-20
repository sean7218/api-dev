from .entry import Entry
from ..bare_block import BareBlock
import types


class SelectOptions(BareBlock):
    TEMPLATE = "kb_blocks/form/select_options.html"
    VALUE_ATTRIBUTE = None
    TITLE_ATTRIBUTE = None
    PLACEHOLDER = None

    def __init__(self,*args,**kwargs):
        if self.VALUE_ATTRIBUTE is None:
            raise Exception("{0} must define self.VALUE_ATTRIBUTE".format(self.getName()))
        if self.TITLE_ATTRIBUTE is None:
            raise Exception("{0} must define self.TITLE_ATTRIBUTE".format(self.getName()))

        super().__init__(*args,**kwargs)

    def get(self,state,data):
        selected_value = self.getValue(state,data)

        options = []
        if self.PLACEHOLDER is not None:
            placeholder = types.SimpleNamespace()
            setattr(placeholder,self.TITLE_ATTRIBUTE,self.PLACEHOLDER)
            if self.TITLE_ATTRIBUTE != self.VALUE_ATTRIBUTE:
                setattr(placeholder,self.VALUE_ATTRIBUTE,"")
            options.append(placeholder)

        options += list(self.getOptions(state,data))

        option_list = []
        for option in options:
            title = getattr(option,self.TITLE_ATTRIBUTE)
            if self.PLACEHOLDER is not None and\
               title == self.PLACEHOLDER:
                value = ""
            else:
                value = getattr(option,self.VALUE_ATTRIBUTE)

            selected = False
            if selected_value is not None and \
               str(selected_value) == str(value):
                selected = True
            if type(selected_value) == type([]):
                if str(value) in [str(v) for v in selected_value]:
                    selected = True

            option = {
                "value": value,
                "title": title,
                "selected": selected,
                }
            option_list.append(option)

        context = super().get(state,data)
        context["options"] = option_list
        return context

    def getOptions(self,state,data):
        raise NotImplementedError


class Select(Entry):
    TAG = "select"
    TEMPLATE = "kb_blocks/form/select.html"
    VALUE_ATTRIBUTE = None
    TITLE_ATTRIBUTE = None
    OPTION_BLOCK = SelectOptions
    MULTIPLE = None # MULTIPLE Enables Select2 Library.

    CSS_LIST = [
        "https://cdnjs.cloudflare.com/ajax/libs/select2/4.0.3/css/select2.min.css",
        ]
    JS_LIST = [
        "https://cdnjs.cloudflare.com/ajax/libs/select2/4.0.3/js/select2.min.js",
        ]

    def __init__(self,*args,**kwargs):
        if self.VALUE_ATTRIBUTE is None:
            raise Exception("{0} must define self.VALUE_ATTRIBUTE".format(self.getName()))
        if self.TITLE_ATTRIBUTE is None:
            raise Exception("{0} must define self.TITLE_ATTRIBUTE".format(self.getName()))

        self.OptionBlock = self.getOptionBlock()
        self.addChild(self.OptionBlock)

        super().__init__(*args,**kwargs)

    def getOptionBlock(self):
        class OptionBlock(self.OPTION_BLOCK):
            PLACEHOLDER = self.PLACEHOLDER
            AUTH = self.AUTH
            VALUE_ATTRIBUTE = self.VALUE_ATTRIBUTE
            TITLE_ATTRIBUTE = self.TITLE_ATTRIBUTE
            
            getOptions = self.getOptions
            getValue = self.getValue

        return OptionBlock

    def get(self,state,data):
        context = super().get(state,data)
        context["content"] = self.renderBlock(self.OptionBlock,state,data)
        return context

    def getAttributes(self,state,data):
        attributes = super().getAttributes(state,data)
        if self.MULTIPLE:
            attributes["multiple"] = self.MULTIPLE
        return attributes

    def getOptions(self,state,data):
        raise NotImplementedError("{0} must implement self.getOptions(state,data)".format(self.getName()))
