from .model_list import ModelList
from .form import Select

from types import SimpleNamespace
from math import ceil


class LimitSelect(Select):
    LIMIT_DEFAULT = None
    LIMIT_OPTIONS = []

    def getValue(self,state,data):
        value = super().getValue(state,data)
        if value is None:
            value = self.LIMIT_DEFAULT
        return value

    def getOptions(self,state,data):
        option_list = []
        for option in self.LIMIT_OPTIONS:
            o = SimpleNamespace()
            o.limit = option
            option_list.append(o)
        return option_list


class Table(ModelList):
    TEMPLATE = "kb_blocks/table.html"
    COLUMNS = [] #A list of names of columns
    COLUMN_NAMES = None #Mapping of the names to the displayed values
    COLUMN_STATES = None #New states that will be created when clicked
    COLUMN_CHANGES = None #State changes that will be created when clicked
    COLUMN_REMOVES = None #State values that will be removed when clicked
    COLUMN_DELETES = None
    COLUMN_SORTS = {} #Columns that are sortable
    LIMIT_SELECT = LimitSelect
    CLASS = "table"
    LIMIT_OPTIONS = [
        10,
        20,
        50,
        100,
        ]
    PAGE_COUNT = 5

    def __init__(self,*args,**kwargs):
        if self.COLUMN_NAMES is None:
            raise Exception("self.COLUMN_NAMES should be a dict that maps values in self.COLUMNS to displayed names")

        self.column_actions = {
            "state": self.COLUMN_STATES,
            "change": self.COLUMN_CHANGES,
            "remove": self.COLUMN_REMOVES,
            "delete": self.COLUMN_DELETES,
            }

        if self.LIMIT_SELECT:
            class LimitSelect(self.LIMIT_SELECT):
                NAME = "{0}_limit_select".format(self.getModelName())
                STATE_KEY = "limit_{0}".format(self.getModelName())
                TITLE_ATTRIBUTE = "limit"
                VALUE_ATTRIBUTE = "limit"
                AUTH = self.AUTH
                LIMIT_DEFAULT = self.LIMIT_DEFAULT
                LIMIT_OPTIONS = self.LIMIT_OPTIONS

            self.limit_select = LimitSelect
            self.addChild(self.limit_select)

        else:
            self.limit_select = None

        super().__init__(*args,**kwargs)

    def get(self,state,data):
        context = super().get(state,data)

        body = []
        for obj in context["model_list"]:
            row = self.makeRow(obj)
            body.append(row)
            
        header = self.getHeader(state)
    
        limit = self.getLimit(state)
        offset = self.getOffset(state)
        model_name = self.getModelName()
        model_count = context["model_count"]

        page_list = self.getPageList(limit,offset,model_name,model_count)
        page_number = self.getPageNumber(limit,offset,model_count)

        if self.limit_select is not None:
            limit_select = self.renderBlock(self.limit_select,state,data)
        else:
            limit_select = None

        context = {
            "header": header,
            "body": body,
            "page_number": page_number,
            "page_list": page_list,
            "limit_select": limit_select,
            }
        return context

    def getHeader(self,state):
        header_list = []
        for col in self.COLUMNS:
            cell = {}
            cell["value"] = self.COLUMN_NAMES[col]
            if col in self.COLUMN_SORTS:
                if self.getModelName() is None:
                    raise Exception("cannot sort without defining self.MODEL_NAME")
                sort_value = self.COLUMN_SORTS[col]
                sort_state = "sort_{0}".format(self.getModelName())
                sort_current_value = state.get(sort_state)
                sort_new_value = None
                if sort_current_value == sort_value:
                    cell["sort"] = 'change="{0}={1}"'.format(sort_state,"-"+sort_value)
                    cell["sort_class"] = "glyphicon glyphicon-sort-by-attributes"
                elif sort_current_value == "-"+sort_value:
                    cell["sort"] = 'remove={0}'.format(sort_state)
                    cell["sort_class"] = "glyphicon glyphicon-sort-by-attributes-alt"
                else:
                    cell["sort"] = 'change="{0}={1}"'.format(sort_state,sort_value)
                cell["sort"] = self.makeTemplateSafe(cell["sort"])
            header_list.append(cell)
        return header_list

    def makeRow(self,obj):
        row = []
        for attr in self.COLUMNS:
            cell = self.makeCell(obj,attr)
            row.append(cell)
        return row

    def makeCell(self,obj,attr):
        value = getattr(obj,attr)

        cell = {
            "value": value,
            }

        action_list = []
        for action in self.column_actions:
            column_dict = self.column_actions[action]
            if column_dict is None:
                continue
            action_dict = column_dict.get(attr)
            if action_dict is None:
                continue
            action_value = self.getAction(action_dict,obj)
            action = '{0}={1}'.format(action,action_value)
            action_list.append(action)

        actions = " ".join(action_list)
        if actions:
            cell["link"] = actions

        return cell

    def getAction(self,action_dict,obj):
        """
        Takes a dict and the object
        returns a url-like querystring
        """
        value_dict = {}
        action = self.getUrl(action_dict)
        for attr, value in action_dict.items():
            if value.startswith("{"):
                value = value.replace("{","").replace("}","")
                value_dict[value] = getattr(obj,value)
        action = action.format(**value_dict)
        return action

    def getPageList(self,limit,offset,model_name,object_count):
        if object_count is None:
            return []

        current_index = int(offset / limit)
        min_index = 0
        max_index = int(ceil(object_count / float(limit)))

        page_start_index = current_index - 2
        if page_start_index < 0:
            page_start_index = 0
        page_end_index = page_start_index + self.PAGE_COUNT
        if page_end_index > max_index:
            page_end_index = max_index
            page_start_index = page_end_index - self.PAGE_COUNT
            if page_start_index < 0:
                page_start_index = 0

        page_list = []

        previous_page = current_index - 1
        if previous_page < 0:
            p_class = "disabled"
        else:
            p_class = ""
        new_offset = previous_page * limit
        page = {
            "number": "Previous",
            "class": p_class,
            "change": "offset_{0}={1}".format(model_name,new_offset)
            }
        page_list.append(page)

        for i in range(page_start_index,page_end_index):
            if i == current_index:
                p_class = "active"
            else:
                p_class = ""
            new_offset = limit * i
            page = {
                "number": i+1,
                "class": p_class,
                "change": "offset_{0}={1}".format(model_name,new_offset)
                }
            page_list.append(page)

        next_page = current_index + 1
        if next_page >= max_index:
            p_class = "disabled"
        else:
            p_class = ""
        new_offset = next_page * limit
        page = {
            "number": "Next",
            "class": p_class,
            "change": "offset_{0}={1}".format(model_name,new_offset)
            }
        page_list.append(page)

        return page_list

    def getPageNumber(self,limit,offset,object_count):
        if limit is None or\
           offset is None or\
           object_count is None:
            return None
        lower = offset + 1
        upper = offset + limit
        if upper > object_count:
            upper = object_count
        return "{0} - {1} of {2}".format(lower,upper,object_count)
