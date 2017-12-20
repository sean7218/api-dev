from ..block import Block


class Entry(Block):
    TEMPLATE = "kb_blocks/form/entry.html"
    TITLE = None
    PLACEHOLDER = None
    CLASS = "form-control"
    VALIDATE = False #Validate without submitting the form
    STATE_KEY = None #Binds value to the state
    DISPLAY_ERROR = True
    CONTENT_CONTAINER = True
    SUBMIT_FUNCTION = "change"
    FUNCTIONS = [
        "submit",
        ]

    def __init__(self,*args,**kwargs):
        if self.STATE_KEY is not None:
            self.addListener(self.STATE_KEY)
        super().__init__(*args,**kwargs)

    def get(self,state,data):
        attributes = self.getAttributes(state,data)

        attributes["id"] = self.getId() + "_entry"
        attributes["name"] = self.getName()

        exception = None
        if self.DISPLAY_ERROR and\
           self.getValue(state,data) is not None:
            try:
                self.validate(state,data)
            except self.UserException as e:
                exception = {
                    "user": str(e),
                    }

        title = self.getTitle(state,data)
        content = self.getEntryContent(state,data)

        context = {
            "title": title,
            "attributes": attributes,
            "content": content,
            "exception": exception,
            }
        return context

    def getAttributes(self,state,data):
        value = self.getValue(state,data)
        attributes = {
            "class": self.CLASS,
            "placeholder": self.PLACEHOLDER,
            "value": value,
            }
        return attributes

    def getTitle(self,state,data):
        return self.TITLE
        
    def getValue(self,state,data):
        value = data.get(self.getName())
        if value is None and self.STATE_KEY:
            value = state.get(self.STATE_KEY)
        return value

    def getEntryContent(self,state,data):
        return None

    def submit(self,state,data):
        if self.VALIDATE:
            self.validate(state,data)
        if self.STATE_KEY:
            self.setState(state,data)

    def validate(self,state,data):
        """
        Determines if the value is good or bad

        If self.validate() is overriden, then the function will be executed when forms are submitted.

        If there is a self.VALIDATE present, then this function will also be hit when the self.VALIDATE trigger is fired on the frontend.

        This means that there may be a situation in which the frontend is not validating the input, but the form is. In that case, you would want to override this function, but leave self.VALIDATE = False

        When there is self.VALIDATE defined, then this function should be overrideen, otherwise the validation is meaningless
        """
        if self.VALIDATE:
            raise NotImplementedError("must override self.validate() when self.VALIDATE is defined")
        return None

    def setState(self,state,data):
        assert self.STATE_KEY is not None

        value = self.getValue(state,data)
        if value is None or value == "":
            state.pop(self.STATE_KEY,None)
        else:
            state[self.STATE_KEY] = value
