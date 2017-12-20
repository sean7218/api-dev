from kb_blocks.blocks import Block, Switch
from kb_blocks.blocks.form import Form, Input, Checkbox, Datetime,\
                                  DeviceId, Email, File, Hidden,\
                                  NotBlank, Password, Select, Text

from types import SimpleNamespace


class FormIntro(Block):
    TEMPLATE = "form_blocks/form_intro.html"
    AUTH = False
    HEADING = "Form Blocks"
    MESSAGE = "Form Blocks take advantage of the underlying block functions to send data to the backend. Specifically, forms implement a self.submit function that is called when the form is submitted."
    STATE_CHANGE = "form_blocks=form_example"
    LINK_TEXT = "Try it"

    def get(self,state,data):
        context = {
            "heading": self.HEADING,
            "message": self.MESSAGE,
            "state_change": self.STATE_CHANGE,
            "link_text": self.LINK_TEXT,
            }
        return context


class NameInput(Input):
    TITLE = "Name"
    AUTH = False

class AgeInput(Input):
    TITLE = "Age"
    AUTH = False

class ExampleForm(Form):
    CHILDREN = [
        NameInput,
        AgeInput,
        ]
    AUTH = False

    def submit(self,state,data):
        print(state,data)

class FormExample(Block):
    TEMPLATE = "form_blocks/form_example.html"
    CHILDREN = [
        ExampleForm,
        ]
    AUTH = False
    HEADING = "Form Example"
    MESSAGE = "This is a simple block that renders a form. The form has two entries. Press the 'submit' button and see what happens in the server output"
    STATE_CHANGE = "form_blocks=form_example_2"
    LINK_TEXT = "See another example"
    FORM_BLOCK = ExampleForm

    def get(self,state,data):
        form = self.renderBlock(self.FORM_BLOCK,state,data)
        context = {
            "heading": self.HEADING,
            "message": self.MESSAGE,
            "state_change": self.STATE_CHANGE,
            "link_text": self.LINK_TEXT,
            "form": form,
            }
        return context

class NameInput2(Input):
    TITLE = "Name"
    AUTH = False

    def validate(self,state,data):
        #Make sure that the name is at least 4 characters long
        value = self.getValue(state,data)
        if len(str(value)) < 4:
            raise self.UserException("Name must be at least 4 characters long")

class AgeInput2(Input):
    TITLE = "Age"
    AUTH = False

    def validate(self,state,data):
        value = self.getValue(state,data)
        #Make sure that the value is a number
        try:
            int(value)
        except ValueError:
            raise self.UserException("age must be a number")
        #Make sure that the value is not less than zero
        if int(value) < 0:
            raise self.UserException("age cannot be less than zero")


class ExampleForm2(Form):
    CHILDREN = [
        NameInput2,
        AgeInput2,
        ]
    AUTH = False

    def submit(self,state,data):
        self.validate(state,data)
        print("val",self.getValue(state,data))

class FormExample2(FormExample):
    CHILDREN = [
        ExampleForm2,
        ]
    HEADING = "Form Example 2"
    MESSAGE = "This is just like the previous example, except that the entries validate when the form is submitted"
    FORM_BLOCK = ExampleForm2
    STATE_CHANGE = "form_blocks=form_example_3"


#The entire example 3 inherits from the example 2 version

class NameInput3(NameInput2):
    VALIDATE = True

class AgeInput3(AgeInput2):
    VALIDATE = True

class ExampleForm3(ExampleForm2):
    CHILDREN = [
        NameInput3,
        AgeInput3,
        ]

class FormExample3(FormExample2):
    CHILDREN = [
        ExampleForm3,
        ]
    FORM_BLOCK = ExampleForm3
    HEADING = "Form Example 3"
    MESSAGE = "This example is a clone of the previous example, except that the fields now validate themselves before the form is submitted. In the souce, the only change is the VALIDATE = True on the input blocks"
    STATE_CHANGE = "form_blocks=form_example_4"


#Example 4 is inherited from example 3

class NameInput4(NameInput3):
    STATE_KEY = "name"

class AgeInput4(AgeInput3):
    STATE_KEY = "age"

class ExampleForm4(ExampleForm3):
    CHILDREN = [
        NameInput4,
        AgeInput4,
        ]

class FormExample4(FormExample3):
    CHILDREN = [
        ExampleForm4,
        ]
    FORM_BLOCK = ExampleForm4
    HEADING = "Form Example 4"
    MESSAGE = "This example is a clone of the previous example, except that the fields now validate themselves before the form is submitted *and* the changes made within the fields are automatically reflected in the state, without the form having to be submitted. In the souce, the only change is the STATE_KEY = 'my_key' on the input blocks"
    STATE_CHANGE = "form_blocks=form_example_5"


#Example 5 is inherited from example 4

class NameInput5(NameInput4):
    STATE_KEY = "name"
    VALIDATE = False

class AgeInput5(AgeInput4):
    STATE_KEY = "age"
    VALIDATE = False

class ExampleForm5(ExampleForm4):
    CHILDREN = [
        NameInput5,
        AgeInput5,
        ]

class FormExample5(FormExample4):
    CHILDREN = [
        ExampleForm5,
        ]
    FORM_BLOCK = ExampleForm5
    HEADING = "Form Example 5"
    MESSAGE = "This example is a clone of the previous example, except that the fields no loger validate themselves before updating the state."
    STATE_CHANGE = "form_blocks=form_example_6"


#Example 6 is inherited from example 5

class NameInput6(NameInput5):
    STATE_KEY = "name"
    DISPLAY_ERROR = False

class AgeInput6(AgeInput5):
    STATE_KEY = "age"
    DISPLAY_ERROR = False

class ExampleForm6(ExampleForm5):
    CHILDREN = [
        NameInput6,
        AgeInput6,
        ]

class FormExample6(FormExample5):
    CHILDREN = [
        ExampleForm6,
        ]
    FORM_BLOCK = ExampleForm6
    HEADING = "Form Example 6"
    MESSAGE = "This example is a clone of the previous example, except that error messages are no longer displayed on the inputs themselves. Submitting the form will still display the form's error message, if any."
    STATE_CHANGE = "form_blocks=form_example_7"


#Example 7

class CheckboxExample(Checkbox):
    TITLE = "Check"
    AUTH = False

class DatetimeExample(Datetime):
    TITLE = "Datetime"
    AUTH = False

class DeviceIdExample(DeviceId):
    AUTH = False

class EmailExample(Email):
    TITLE = "Email"
    AUTH = False

class FileExample(File):
    TITLE = "File"
    AUTH = False

class HiddenExample(Hidden):
    AUTH = False

class PasswordExample(Password):
    TITLE = "Password"
    AUTH = False

class SelectExample(Select):
    TITLE = "Select"
    TITLE_ATTRIBUTE = "id"
    VALUE_ATTRIBUTE = "name"
    AUTH = False
    PLACEHOLDER = "Please select"

    def getOptions(self,state,data):
        options = []
        for i in range(10):
            option = SimpleNamespace()
            option.id = i
            option.name = i
            options.append(option)
        return options

class TextExample(Text):
    TITLE = "Text"
    AUTH = False

class ExampleForm7(Form):
    AUTH = False
    CHILDREN = [
        NameInput,
        AgeInput,
        CheckboxExample,
        DatetimeExample,
        DeviceIdExample,
        EmailExample,
        FileExample,
        HiddenExample,
        PasswordExample,
        SelectExample,
        TextExample,
        ]

    def submit(self,state,data):
        print(self.getValue(state,data))

class FormExample7(FormExample6):
    CHILDREN = [
        ExampleForm7,
        ]
    FORM_BLOCK = ExampleForm7
    HEADING = "Form Example 7"
    MESSAGE = "This an example of all core form types."
    STATE_CHANGE = "content=auth_blocks"

#Main app

class FormBlocks(Switch):
    AUTH = False
    CHILDREN = [
        FormIntro,
        FormExample,
        FormExample2,
        FormExample3,
        FormExample4,
        FormExample5,
        FormExample6,
        FormExample7,
        ]
