from kb_blocks.blocks import Block, ModelList, ModelView, Table

from kb_blocks.blocks.form import Form, Input, Checkbox, Datetime, \
    DeviceId, Email, File, Hidden, \
    NotBlank, Password, Select, Text

from types import SimpleNamespace

from kblock.models import Stack
from django.shortcuts import redirect

class NameInput(Input):
    TITLE = "Name"
    AUTH = False


class BalanceInput(Input):
    TITLE = "Balance"
    AUTH = False


class GoalInput(Input):
    TITLE = "Goal"
    AUTH = False


class CategorySelect(Select):
    TITLE = "Category"
    TITLE_ATTRIBUTE = "id"
    VALUE_ATTRIBUTE = "name"
    AUTH = False
    PLACEHOLDER = "Please select"

    def getOptions(self, state, data):
        options = ['Family', 'Work', 'Personal', 'Retirement']
        output = []
        for i in range(4):
            option = SimpleNamespace()
            option.id = options[i]
            option.name = options[i]
            output.append(option)
        return output


class OwnerSelect(Select):
    TITLE = "Owner"
    TITLE_ATTRIBUTE = "id"
    VALUE_ATTRIBUTE = "name"
    AUTH = False
    PLACEHOLDER = "Please select"

    def getOptions(self, state, data):
        options = ['Sean', 'Lucy', 'Michael', 'Josh']
        output = []
        for i in range(4):
            option = SimpleNamespace()
            option.id = options[i]
            option.name = options[i]
            output.append(option)
        return output


class CreateStackForm(Form):
    AUTH = False
    CHILDREN = [
        NameInput,
        BalanceInput,
        GoalInput,
        CategorySelect,
        OwnerSelect,
    ]

    def submit(self, state, data):
        print(self.getValue(state, data))
        form_values = self.getValue(state, data)
        name = form_values['name_input']
        balance = form_values['balance_input']
        goal = form_values['goal_input']
        category = form_values['category_select']
        owner = form_values['owner_select']

        stack = Stack(None, name, balance, goal, category, owner)
        stack.save()


class FormBlock(Block):
    TEMPLATE = "dashboard_block/form.html"
    CHILDREN = [
        CreateStackForm,
    ]
    AUTH = False
    HEADING = "Form Example"
    MESSAGE = "This is a simple block that renders a form. The form has two entries." \
              "Press the 'submit' button and see what happens in the server output "
    STATE_CHANGE = "form_blocks=form_example_2"
    LINK_TEXT = "See another example"
    FORM_BLOCK = CreateStackForm

    def get(self, state, data):
        form = self.renderBlock(self.FORM_BLOCK, state, data)
        context = {
            "heading": self.HEADING,
            "message": self.MESSAGE,
            "state_change": self.STATE_CHANGE,
            "link_text": self.LINK_TEXT,
            "form": form,
        }
        return context


class TableBlock(Table):
    TEMPLATE = "dashboard_block/stacks.html"
    AUTH = False
    MODEL = Stack
    COLUMNS = [
        "id",
        "name",
        "goal",
        "balance",
        "category",
        "owner",
    ]
    COLUMN_NAMES = {
        "id": "ID",
        "name": "Name",
        "goal": "Goal",
        "balance": "Balance",
        "category": "Category",
        "owner": "Owner",
    }
    COLUMN_SORTS = {
        "id": "id",
        "name": "name",
        "category": "category",
        "owner": "owner",
    }



class DashboardBlock(Block):
    TEMPLATE = "dashboard_block/dashboard.html"
    AUTH = False
    HEADING = "Render Block"
    MESSAGE = "This block is just like the other 2 blocks, but the main control center is there where you can " \
              "edit, delete, create, view. There block has two children blocks passed in i.e. (FormBlock TableBlock). " \
              "Inside the FormBlock, you can create a stack but you have manually refresh the page with the browser ," \
              "because I haven't figure out the redirect inside the class Block. " \
              "The edit and delete button uses the listener and display the current selected the item fetched from " \
              "MySQL. All the records were persisted using MySQL and defined in the .model file. "
    STATE_CHANGE = "switch_blocks=dashboard_block"
    LINK_TEXT = "Check out Render Many Blocks"
    RENDERED_BLOCK = TableBlock
    RENDERED_BLOCK2 = FormBlock
    CHILDREN = [
        RENDERED_BLOCK,
        RENDERED_BLOCK2,
    ]

    LISTENERS = [
        "number_1",
        "edit",
        "delete",
        ]

    def getRecord(self, atIndex):
        record = Stack.objects.get(pk=atIndex)
        return record

    def get(self, state, data):

        edit_number = state.get("edit", 1)
        delete_number = state.get("delete", 1)

        data["edit"] = edit_number
        data["delete"] = delete_number

        record_edit = self.getRecord(edit_number)
        record_delete = self.getRecord(delete_number)

        rendered_block = self.renderBlock(self.RENDERED_BLOCK, state, data)
        rendered_block2 = self.renderBlock(self.RENDERED_BLOCK2, state, data)
        context = {
            "heading": self.HEADING,
            "message": self.MESSAGE,
            "state_change": self.STATE_CHANGE,
            "link_text": self.LINK_TEXT,
            "rendered_block": rendered_block,
            "rendered_block2": rendered_block2,
            "record_edit": record_edit,
            "record_delete": record_delete,
        }
        return context


