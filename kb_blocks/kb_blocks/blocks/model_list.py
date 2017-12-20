from .block import Block
import json
from django.db.models import Q


class ModelList(Block):
    MODEL = None
    MODEL_NAME = None
    LIMIT_DEFAULT = 20
    MODEL_VIEW = None
    SORT_DEFAULT = None
    SEARCH_FIELDS = []
    FILTER_KEY = "{0}__icontains"
    FUNCTIONS = [
        "create",
        "update",
        ]

    def __init__(self,*args,**kwargs):
        if self.MODEL is None:
            raise Exception("{0} does not define self.MODEL".format(self.getName()))

        if self.MODEL_VIEW is not None:
            self.addChild(self.MODEL_VIEW)
            self.MODEL = self.MODEL_VIEW.MODEL

        self.model_name = self.getModelName()
        
        self.list_name = "{0}_list".format(self.model_name)

        self.limit_param = "limit_{0}".format(self.model_name)
        self.addListener(self.limit_param)
        self.offset_param = "offset_{0}".format(self.model_name)
        self.addListener(self.offset_param)
        self.sort_param = "sort_{0}".format(self.model_name)
        self.addListener(self.sort_param)
        self.search_param = "search_{0}".format(self.model_name)
        self.addListener(self.search_param)

        super().__init__(*args,**kwargs)

    def getModelName(self):
        if self.MODEL_NAME is None:
            model_name = self.MODEL.__name__
            return self.convertToUnderscoreCase(model_name)
        else:
            return self.MODEL_NAME

    def get(self,state,data):
        model_list,model_count = self.query(state,data)

        #Get the next and previous
        offset = self.getOffset(state)
        limit = self.getLimit(state)
        next_offset = self.getNextOffset(state)
        previous_offset = self.getPreviousOffset(state)

        model_list = list(model_list)

        context = {
            "model_list": model_list,
            "model_count": model_count,
            "next_offset": next_offset,
            "previous_offset": previous_offset,
            }
        return context

    def create(self,state,data):
        if self.MODEL_VIEW is None:
            raise Exception("must define self.MODEL_VIEW to call self.create()")
        return self.createUpdate(state,data,self.MODEL_VIEW.create)

    def update(self,state,data):
        if self.MODEL_VIEW is None:
            raise Exception("must define self.MODEL_VIEW to call self.update()")
        return self.createUpdate(state,data,self.MODEL_VIEW.update)

    def createUpdate(self,state,data,function):
        model_view = self.initBlock(self.MODEL_VIEW)
        obj_list = self.getObjectList(data)

        new_obj_list = []
        for obj in obj_list:
            data.update(obj)
            function(model_view,state,data)
            new_obj = data[model_view.model_name]
            new_obj_list.append(new_obj)

        context = {
            "model_list": new_obj_list,
            }
        return context

    def getObjectList(self,data):
        obj_list = data.get(self.list_name)
        if obj_list is None:
            raise self.ArgumentException("must provide {0} in request".format(self.list_name))

        if not isinstance(obj_list,list):
            raise self.ArgumentException("{0} must be a list".format(self.list_name))

        return obj_list
    
    def query(self,state,data):
        q = self.getQueryset(state,data)

        split_value = "{0}__".format(self.model_name)
        for s in state:
            if split_value not in s:
                continue

            split_arg = s.split(split_value)
            filter_arg = split_arg[1]
            filter_value = state[s]

            filter_dict = {filter_arg: filter_value}
            try:
                q = q.filter(**filter_dict)
            except Exception as e:
                raise self.ArgumentException("bad filter: {0}: {1}".format(filter_dict,e))

        #Search
        search = self.getSearch(state)
        if search is not None:
            if not self.SEARCH_FIELDS:
                raise Exception("block {0} does not define any self.SEARCH_FIELDS".format(self.getName()))
            search = str(search)
            search_words = search.split(" ")
            filters = Q()
            for word in search_words:
                word_filters = Q()
                for fileld in self.SEARCH_FIELDS:
                    filter_key = self.FILTER_KEY.format(fileld)
                    filter_dict = {
                        filter_key: word,
                        }
                    word_filters |= Q(**filter_dict)
                filters &= word_filters
            q = q.filter(filters).distinct()

        #Count
        count = q.count()

        #Sort
        sort = state.get(self.sort_param)
        if sort is not None:
            q = q.order_by(sort)

        #Page
        offset = state.get(self.offset_param)
        limit = state.get(self.limit_param)
        if offset is None:
            offset = 0
        if limit is None:
            limit = self.LIMIT_DEFAULT
        offset = int(offset)
        limit = int(limit)
        start_index = offset
        end_index = offset + limit
        q = q[start_index:end_index]

        return q,count

    def getQueryset(self,state,data):
        q = self.MODEL.objects.all()
        return q

    def getLimit(self,state):
        return state.get(self.limit_param,self.LIMIT_DEFAULT)

    def getOffset(self,state):
        return state.get(self.offset_param,0)

    def getNextOffset(self,state):
        current_offset = self.getOffset(state)
        limit = self.getLimit(state)
        next_offset = current_offset + limit
        return next_offset

    def getPreviousOffset(self,state):
        current_offset = self.getOffset(state)
        limit = self.getLimit(state)
        previous_offset = current_offset - limit
        if previous_offset < 0:
            previous_offset = 0
        return previous_offset
        
    def getSort(self,state):
        return state.get(self.sort_param,self.SORT_DEFAULT)

    def getSearch(self,state):
        return state.get(self.search_param)
