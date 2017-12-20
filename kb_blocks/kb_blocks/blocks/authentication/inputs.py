from ..form import Input, Email, Password, NotBlank


class UsernameInput(Input,NotBlank):
    AUTH = False
    TITLE = "Username"
    PLACEHOLDER = "username"
    VALIDATE = True
    VALIDATE_EXEPTION_NOT_BLANK = "No username given"

class EmailInput(Email):
    AUTH = False
    TITLE = "Email"
    PLACEHOLDER = "Email"

class PasswordInput(Password):
    AUTH = False
    TITLE = "Password"
    PLACEHOLDER = "Password"

class PasswordConfirmInput(Password):
    AUTH = False
    TITLE = "Confirm Password"
    PLACEHOLDER = "Confirm Password"
    MASTER_INPUT = PasswordInput

    def __init__(self,*args,**kwargs):
        if self.MASTER_INPUT is None:
            raise Exception("must define self.MASTER_INPUT")

        super().__init__(*args,**kwargs)

        self.addChild(self.MASTER_INPUT)

    def validate(self,state,data):
        master_value = self.initBlock(self.MASTER_INPUT).getValue(state,data)
        value = self.getValue(state,data)
        if value != master_value:
            raise self.UserException("Passwords do not match")
