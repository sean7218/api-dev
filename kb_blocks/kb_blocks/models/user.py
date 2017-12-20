from ..blocks.block import Block
import random


from django.contrib.auth.models import User as BaseUser
from django.contrib.auth import authenticate, login, logout


class User(BaseUser):
    ERROR_ACCOUNT_DISABLED = "The account is disabled"
    ERROR_CREDENTIALS = "The credentials were incorrect"

    class Meta:
        abstract = True

    def __unicode__(self):
        return self.username

    def save(self,*args,**kwargs):
        if not self.id:
            #Set the password
            self.set_password(self.password)
            if not self.username:
                #Make a temp username
                username = str(random.random())[:30]
                self.username = username
                #Save the model
                BaseUser.save(self)
                #Create the real username from the id
                self.username = "user{0}".format(self.id)
                #Save the model again
        super().save(*args,**kwargs)


    #Framework-specific functions

    def updatePassword(self,password):
        if not self.id:
            raise Exception("This method can only be called on Users that have been saved previously")
        self.set_password(password)

    def signIn(self,request,password):
        user = authenticate(username=self.username,password=password)
        if user is not None:
            #The password verified for the user
            if user.is_active:
                login(request,user)
            else:
                raise Block.UserException(self.ERROR_ACCOUNT_DISABLED)
        else:
            #The authentication system was unable to verify the username and password
            raise Block.UserException(self.ERROR_CREDENTIALS)

    def signOut(self,request):
        logout(request)
