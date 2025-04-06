from .fmt import *
from ..._hycore.better_descriptor import BetterDescriptor, BetterDescriptorInstance


class ApiFunctionInstance(BetterDescriptorInstance):
    def __init__(self, rst: RequestFmt, rps: ResponseFmt, parent: "ApiFunction" = None):
        super().__init__()
        self.parent = parent

        self.rst_fmt = rst
        self.rps_fmt = rps

        self.method = parent.method
        self.target = parent.target

        self.url = parent.base_url + self.target

    def __better_get__(self, instance, owner, parent) -> Any:
        return self

    def __call__(self, **kwargs):
        data = self.rst_fmt.generate(self.rps_fmt, **kwargs)  # 先生成请求数据
        data = self.parent.serializer.serialize(data, **kwargs)  # 对初始的数据进行序列化
        rsp_code, rsp_data = self.parent.requester.request(self.method, self.url, data)  # 发送请求
        fmt_data = self.rps_fmt.generate(rsp_code, rsp_data)  # 生成响应数据
        fmt_data = self.parent.serializer.deserialize(fmt_data, **kwargs)  # 反序列化
        processed_data = self.parent.processor.process(fmt_data)  # 处理响应数据
        return processed_data


class ApiFunction(BetterDescriptor):
    instance_type = ApiFunctionInstance

    base_url: str = None

    def __better_new__(self) -> "BetterDescriptorInstance":
        return ApiFunctionInstance(self.rst_fmt, self.rps_fmt, self)

    def __better_init__(self, name, owner):
        self.serializer = owner.backend.__api_serializer__
        self.requester = owner.backend.__api_requester__
        self.processor = owner.backend.__api_processor__

    def __init__(self, target_path, request: RequestFmt, response: ResponseFmt, method='GET'):
        super().__init__()
        self.target = target_path
        self.rst_fmt = request
        self.rps_fmt = response
        self.method = method
