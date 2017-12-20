from .form_content import FormContent


class Form(FormContent):
    TEMPLATE = "kb_blocks/form/form.html"
    CLASS = ""
    BUTTON_CLASS = "btn btn-primary"
    BUTTON_TITLE = "Submit"
    ALERT_CLASS = "alert alert-danger"
    FUNCTIONS = [
        "submit",
        ]
    
    def submit(self,state,data):
        raise NotImplementedError
