from .input import Input

import re


class Email(Input):
    VALIDATE_REGEX = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    EXCEPTION_MESSAGE_BAD_EMAIL = "Please enter a valid email address"

    def validate(self,state,data):
        value = self.getValue(state,data)
        if not re.match(self.VALIDATE_REGEX,value):
            raise self.UserException(self.EXCEPTION_MESSAGE_BAD_EMAIL)
