from ..api_abc import API_Processor
from ..._hycore.type_func import AttrDict


class ObjectiveJsonProcessor(API_Processor):
    def process(self, rps_code, rps_data):
        for key, value in list(rps_data.items()):
            if isinstance(value, dict):
                self.process(rps_code, value)
                rps_data[key] = AttrDict(**value)
        return rps_data
