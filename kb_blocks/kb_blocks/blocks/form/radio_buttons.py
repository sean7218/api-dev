from .entry import Entry
from .input import Input
from .checkbox import Checkbox
from .select import SelectOptions


class RadioButton(Checkbox):
    TYPE = "radio"

    def getName(self):
        return self.parent_block.getName()

    def getValue(self,state,data):
        return super().getName()

    def getAttributes(self,state,data):
        attributes = Input.getAttributes(self,state,data)
        if self.getChecked(state,data):
            attributes["checked"] = 1
        else:
            attributes.pop("checked",None)
        return attributes

    def getChecked(self,state,data):
        return str(data.get(self.getName())) == str(self.getValue(state,data))

class RadioButtons(SelectOptions,Entry):
    TEMPLATE = "kb_blocks/form/radio_buttons.html"
    RADIO_BUTTON_BLOCK = RadioButton
    OPTION_CLASS = "container-radio-option"

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        
        if self.RADIO_BUTTON_BLOCK is None:
            raise Exception("{0} must define self.RADIO_BUTTON_BLOCK".format(self.getName()))
        if self.PLACEHOLDER is not None:
            raise Exception("{0} RadioOptions cannot define self.PLACEHOLDER".format(self.getName()))

        self.addChild(self.RADIO_BUTTON_BLOCK)

    def get(self,state,data):
        context = super().get(state,data)

        options = []
        for option in context["options"]:
            Radio = self.getRadioButton(state,data,option)
            o = self.renderBlock(Radio,state,data)
            options.append(o)

        context = {
            "options": options,
            }
        return context

    def getValue(self,state,data):
        options = self.getOptions(state,data)
        value = data.get(self.getName())
        for option in options:
            if getattr(option,self.VALUE_ATTRIBUTE) == value:
                return value
        return None

    def getRadioButton(self,state,data,option):
        class Radio(RadioButton):
            NAME = str(option["value"])
            TITLE = str(option["title"])
            AUTH = self.AUTH
        self.addChild(Radio)
        return Radio
