from .input import Input
import datetime


class Datetime(Input):
    TEMPLATE = "kb_blocks/form/datetime.html"
    CLASS = "form-control flatpickr"
    JS_LIST = [
        "https://cdnjs.cloudflare.com/ajax/libs/flatpickr/3.0.7/flatpickr.min.js"
        ]
    CSS_LIST = [
        "https://cdnjs.cloudflare.com/ajax/libs/flatpickr/3.0.7/flatpickr.min.css",
        ]

    def getValue(self,state,data):
        value = super().getValue(state,data)
        if isinstance(value,(datetime.date,datetime.datetime)):
            value = value.isoformat()
        return value
