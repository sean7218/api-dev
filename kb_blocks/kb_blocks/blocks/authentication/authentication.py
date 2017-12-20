from ..switch import Switch
from .sign_up import SignUpForm
from .sign_in import SignInForm


class Authentication(Switch):
    AUTH = False
    TEMPLATE = "kb_blocks/authentication.html"
    SIGN_IN_FORM = SignInForm
    SIGN_UP_FORM = SignUpForm
    DEFAULT_BLOCK = SignInForm
    
    def __init__(self,*args,**kwargs):
        self.SignUpForm = self.getSignUpForm()
        if self.SignUpForm is not None:
            self.addChild(self.SignUpForm)
            if self.DEFAULT_BLOCK == self.SIGN_UP_FORM:
                self.DEFAULT_BLOCK = self.SignUpForm

        self.SignInForm = self.getSignInForm()
        if self.SignInForm is not None:
            self.addChild(self.SignInForm)
            if self.DEFAULT_BLOCK == self.SIGN_IN_FORM:
                self.DEFAULT_BLOCK = self.SignInForm

        super().__init__(*args,**kwargs)
        
    def getSignUpForm(self):
        if self.SIGN_UP_FORM:
            class SignUpForm(self.SIGN_UP_FORM):
                AUTH = False
                signUp = type(self).signUp
            return SignUpForm

    def getSignInForm(self):
        if self.SIGN_IN_FORM:
            class SignInForm(self.SIGN_IN_FORM):
                AUTH = False
                signIn = type(self).signIn
            return SignInForm

    def get(self,state,data):
        context = super().get(state,data)
        if self.SIGN_IN_FORM:
            sign_in = self.initBlock(self.SignInForm)
            sign_in.name = sign_in.getName()
            context["sign_in_form"] = sign_in
        if self.SIGN_UP_FORM:
            sign_up = self.initBlock(self.SignUpForm)
            sign_up.name = sign_up.getName()
            context["sign_up_form"] = sign_up
        return context

    def signUp(self,state,data):
        raise NotImplementedError()

    def signIn(self,state,data):
        raise NotImplementedError()
