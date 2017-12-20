from kbde.data import Serializer, TypeSerializer
from django.db import models
from django.http.request import HttpRequest


class ModelSerializer(TypeSerializer):
    TYPES = (
        models.Model,
        )

    def serialize(self,model):
        model_data = {}
        for key,value in model.__dict__.items():
            if key.startswith("_"):
                continue
            if isinstance(value,(models.Model,
                                 models.query.QuerySet)):
                continue
            model_data[key] = value
        return self.parent_serialize(model_data)

class RequestSerializer(TypeSerializer):
    TYPES = (
        HttpRequest,
        )

    def serialize(self,request):
        return None


class KbBlocksSerializer(Serializer):
    SERIALIZERS = Serializer.SERIALIZERS + (
        ModelSerializer,
        RequestSerializer,
        )
    BLOCK_GET_CONTENT_ATTR = "getContent"

    def serialize(self,data):
        content_function = getattr(data,self.BLOCK_GET_CONTENT_ATTR,None)
        if callable(content_function):
            return self.serialize(content_function())
        return super().serialize(data)
