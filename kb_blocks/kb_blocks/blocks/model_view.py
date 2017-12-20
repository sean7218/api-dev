from .block import Block
from kbde.data import Serializer
from django.db import utils


class ModelView(Block):
    MODEL = None
    MODEL_NAME = None
    FIELDS = []
    FUNCTIONS = [
        "create",
        "update",
        "delete",
        ]

    def __init__(self,*args,**kwargs):
        if self.MODEL is None:
            raise Exception("{0} does not define self.MODEL".format(self.getName()))

        self.model_name = self.getModelName()
        self.state_param = "{0}_id".format(self.model_name)
        self.add_models_prefix = "add_{0}_".format(self.model_name)
        self.remove_models_prefix = "remove_{0}_".format(self.model_name)
        
        super().__init__(*args,**kwargs)

    def getModelName(self):
        if self.MODEL_NAME is None:
            model_name = self.MODEL.__name__
            return self.convertToUnderscoreCase(model_name)
        else:
            return self.MODEL_NAME

    def getListeners(self):
        listeners = Block.getListeners(self)
        listeners.append(self.state_param)
        return listeners

    def get(self,state,data):
        #Check to see if a model instance has been passed in via data
        model = data.get(self.model_name)
        if model is None:
            model_id = state.get(self.state_param)
            if model_id is None:
                #Could not get id
                raise self.ArgumentException("{0} could not get model_id".format(self.getName()))
            model = self.queryModel(self.MODEL,model_id)

        context = {
            "model": model,
            }
        return context

    def create(self,state,data):
        model = self.getNewModel(self.MODEL)
        model = self.setModelData(model,data,True)
        self.saveModel(model)
        data[self.model_name] = model
        state[self.state_param] = model.id

    def update(self,state,data):
        model = self.read(state,data)["model"]
        if model is None:
            raise self.ArgumentException("{0} could not get model to update".format(self.name))

        #Get the add variable if it exists
        for key,value in data.items():
            if key.startswith(self.add_models_prefix):
                self.addModels(model,key,value)
                data[self.model_name] = model
                return None

        #Get the remove variable is it exists
        for key,value in data.items():
            if key.startswith(self.remove_models_prefix):
                self.removeModels(model,key,value)
                data[self.model_name] = model
                return None

        model = self.setModelData(model,data)
        self.saveModel(model)
        data[self.model_name] = model

    def addModels(self,model,add_key,model_id_list):
        if not isinstance(model_id_list,list):
            raise self.ArgumentException("{0} was not a list".format(add_key))
        many_to_many_attribute = "_".join(add_key.split("_")[2:])
        many_to_many_field = getattr(model,many_to_many_attribute,None)
        if many_to_many_field is None:
            raise self.ArgumentException("{0} does not have a memeber called {1}".format(self.model_name,many_to_many_attribute))
        many_to_many_field.add(*model_id_list)

    def removeModels(self,model,remove_key,model_id_list):
        if not isinstance(model_id_list,list):
            raise self.ArgumentException("{0} was not a list".format(add_key))
        many_to_many_attribute = "_".join(remove_key.split("_")[2:])
        many_to_many_field = getattr(model,many_to_many_attribute,None)
        if many_to_many_field is None:
            raise self.ArgumentException("{0} does not have a memeber called {1}".format(self.model_name,many_to_many_attribute))
        many_to_many_field.remove(*model_id_list)

    def setModelData(self,model,data,create=False):
        """
        When creating a new model, we only assign attributes that are present in the data. This allows default field values to be defined in the models.
        When updating a model, we assign all attributes that are present in self.FIELDS. If an attribute is not present in the data, it is considered to be `None`
        """
        for field in self.FIELDS:
            if create and field not in data:
                continue
            value = data.get(field)
            setattr(model,field,value)
        return model

    def delete(self,state,data):
        #Get the model that I want to delete
        model = self.read(state,data)["model"]
        if model is None:
            raise self.ArgumentException("{0} could not get model to delete".format(self.name))
        self.deleteModel(model)
        data[self.model_name] = model
        state.pop(self.state_param,None)

    #ORM-specific functions
        
    def queryModel(self,model,model_id):
        try:
            m = model.objects.get(id=model_id)
        except model.DoesNotExist:
            raise self.NotFoundException("could not find {0} with id {1}".format(model.__class__.__name__,model_id))
        return m

    def getNewModel(self,model):
        return model()

    def saveModel(self,model):
        try:
            model.save()
        except utils.IntegrityError as e:
            raise self.ArgumentException(str(e))

    def deleteModel(self,model):
        model.delete()
