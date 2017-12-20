from kb_blocks.blocks import Block, Switch
from kb_blocks.blocks.authentication import Authentication

#Just regular django stuff
from django.contrib.auth.models import User
from django.contrib.auth import login, logout


class NeedsLogin(Block):
    TEMPLATE = "auth_blocks/needs_login.html"
    FUNCTIONS = [
        "signOut",
        ]

    def signOut(self,state,data):
        logout(self.request)
        state.clear()


class Authentication(Authentication):
    TEMPLATE = "auth_blocks/authentication.html"

    def signUp(self,state,data):
        print("signed up")

    def signIn(self,state,data):
        """
        For this, any password will work.
        All users are signed in with the same fake user.
        """
        
        try:
            user = User.objects.all()[0]
        except IndexError:
            user = User()
            user.save()

        login(self.getRequest(),user)

        print("signed in")

        state.clear()


class AuthBlocks(Switch):
    AUTH = False
    CHILDREN = [
        Authentication,
        ]
