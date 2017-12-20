from ..form import Form
from .inputs import EmailInput,\
                    PasswordInput,\
                    PasswordConfirmInput


class SignUpForm(Form):
    AUTH = False
    USERNAME_INPUT = None
    EMAIL_INPUT = EmailInput
    PASSWORD_INPUT = PasswordInput
    PASSWORD_CONFIRM_INPUT = PasswordConfirmInput

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        if self.USERNAME_INPUT:
            self.addChild(self.USERNAME_INPUT)
        if self.EMAIL_INPUT:
            self.addChild(self.EMAIL_INPUT)
        self.addChild(self.PASSWORD_INPUT)
        self.addChild(self.PASSWORD_CONFIRM_INPUT)

    def submit(self,state,data):
        self.validate(state,data)
        self.signUp(state,data)

    def signUp(self,state,data):
        """
        Performs the actual process of signing the user up
        """
        raise NotImplementedError()
