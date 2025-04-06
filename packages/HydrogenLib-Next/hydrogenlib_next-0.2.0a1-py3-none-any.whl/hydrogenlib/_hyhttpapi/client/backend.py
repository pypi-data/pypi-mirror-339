from .processor import ObjectiveJsonProcessor
from .requester import BasicRequester
from ..api_abc import API_Backend


class JsonBackend(API_Backend):
    __api_processor__ = ObjectiveJsonProcessor()
    __api_requester__ = BasicRequester()
    __api_serializer__ = None
