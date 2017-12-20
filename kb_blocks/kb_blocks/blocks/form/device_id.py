from .hidden import Hidden
from ...common.random import getRandom


class DeviceId(Hidden):
    TEMPLATE = "kb_blocks/form/device_id.html"
    
    def get(self,state,data):
        context = {
            "random": self.getRandom(),
            }
        context.update(super().get(state,data))
        return context

    def getRandom(self):
        return getRandom(16)
