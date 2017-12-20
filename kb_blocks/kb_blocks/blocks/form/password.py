from .input import Input
from .not_blank import NotBlank


class Password(Input,NotBlank):
    TAG = "input"
    TYPE = "password"
    EXCEPTION_MESSAGE_NOT_BLANK = "Password cannot be empty"

    def __init__(self,*args,**kwargs):
        if self.STATE_KEY:
            raise Exception("Password entries cannot set `STATE_KEY = True`")
        return super().__init__(*args,**kwargs)
