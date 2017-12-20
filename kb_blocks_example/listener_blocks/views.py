from kb_blocks.blocks import Switch, Block


class ListenerIndex(Block):
    AUTH = False
    TEMPLATE = "listener_blocks/listener_index.html"


class ListenerExample1(Block):
    AUTH = False
    TEMPLATE = "listener_blocks/listener_example_1.html"
    COLOR_DEFAULT = "red"
    LISTENERS = [
        "background",
        ]

    def get(self,state,data):
        color = state.get("background",self.COLOR_DEFAULT)
        context = {
            "background": color,
            }
        return context

class ListenerExample2(Block):
    AUTH = False
    TEMPLATE = "listener_blocks/listener_example_2.html"
    NUMBER_PARAM = "number_1"
    LISTENERS = [
        "number_1",
        ]

    def get(self,state,data):
        number = state.get(self.NUMBER_PARAM)
        context = {
            "number": number,
            }
        return context

class ListenerExample3(ListenerExample2):
    AUTH = False
    TEMPLATE = "listener_blocks/listener_example_3.html"
    NUMBER_PARAM = "number_2"
    LISTENERS = [
        "number_2",
        ]

class ListenerExample4(Block):
    AUTH = False
    TEMPLATE = "listener_blocks/listener_example_4.html"
    LISTENERS = [
        "number_1",
        "number_2",
        ]

    def get(self,state,data):
        number_1 = state.get("number_1",0)
        number_2 = state.get("number_2",0)
        data["number_1"] = number_1
        data["number_2"] = number_2

        try:
            return self.calculateSum(state,data)
        except self.UserException as e:
            context = {
                "error": e,
                }
            return context

        return super().get(state,data)
            
    def calculateSum(self,state,data):
        try:
            number_1 = data["number_1"]
            number_2 = data["number_2"]
            number_1 = int(number_1)
            number_2 = int(number_2)
        except ValueError:
            state["background"] = "red"
            raise self.UserException("Numbers must be integers")
        except AttributeError:
            raise self.ArgumentException("must provide number_1 and number_2")

        if not number_1 and not number_2:
            state["background"] = "yellow"
        else:
            state["background"] = "green"

        context = {
            "sum": number_1 + number_2,
            }
        return context


class ListenerExample(Block):
    AUTH = False
    TEMPLATE = "listener_blocks/listener_example.html"
    CHILDREN = [
        ListenerExample1,
        ListenerExample2,
        ListenerExample3,
        ListenerExample4,
        ]

    def get(self,state,data):
        example_list = []
        for c in self.getChildren():
            c = self.renderBlock(c,state,data)
            example_list.append(c)

        numbers = range(10)

        context = {
            "example_list": example_list,
            "numbers": numbers,
            }
        return context


class ListenerBlocks(Switch):
    AUTH = False
    CHILDREN = [
        ListenerIndex,
        ListenerExample,
        ]
