from kb_blocks.blocks import Block, Switch, ModelList, ModelView, Table
from .models import Person

import random


class ModelIntro(Block):
    AUTH = False
    TEMPLATE = "model_blocks/model_intro.html"


class ModelViewExample(ModelView):
    AUTH = False
    TEMPLATE = "model_blocks/model_view_example.html"
    MODEL = Person


class ModelListExample(ModelList):
    AUTH = False
    TEMPLATE = "model_blocks/model_list_example.html"
    MODEL = Person
    CREATE_MODEL_COUNT = 1000

    def get(self,state,data):
        #Check to make sure that there are at least 3 models in the db
        if self.MODEL.objects.count() < self.CREATE_MODEL_COUNT:
            for i in range(self.CREATE_MODEL_COUNT):
                model = self.MODEL()
                model.name = random.random()
                model.age = random.choice(range(100))
                model.save()
        return super().get(state,data)


class TableExample(Table):
    TEMPLATE = "model_blocks/table_example.html"
    AUTH = False
    MODEL = Person
    COLUMNS = [
        "id",
        "name",
        "age",
        ]
    COLUMN_NAMES = {
        "id": "ID",
        "name": "Name",
        "age": "Age",
        }
    COLUMN_SORTS = {
        "id": "id",
        "name": "name",
        "age": "age",
        }


class ModelBlocks(Switch):
    AUTH = False
    CHILDREN = [
        ModelIntro,
        ModelListExample,
        ModelViewExample,
        TableExample,
        ]
