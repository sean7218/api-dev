from .entry import Entry


class NotBlank(Entry):
    """
    This is an entry mixin with a built-in validator that checks to make sure that the value is not blank.
    It cannot be used on its own, and must be used with another Entry subclass
    """
    EXCEPTION_MESSAGE_NOT_BLANK = "Field cannot be empty"
    
    def validate(self,state,data):
        value = self.getValue(state,data)
        if not str(value):
            raise self.UserException(self.EXCEPTION_MESSAGE_NOT_BLANK)
