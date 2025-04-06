import typing
from threading import Lock
from typing import Optional, Union

from .actions import pack_attr, unpack_attr
from .errors import *
from .. import abc
from ...._hycore.type_func import get_qualname, get_subclasses_recursion

SimpleTypes = typing.Union[int, str, bytes, float]


class BinStructBase:
    """

    # 二进制结构体基类

    方法:
        - pack() **不可覆写**, 打包结构体
        - unpack(data) 解包结构体
    属性:
        - _data_ 需要打包的属性**列表**

    """
    __data__ = []  # Variables' names

    def pack_event(self, *args, **kwargs):
        """
        打包事件,进行打包前的处理
        """
        return True

    def pack_attr_event(self, attr_name: str):
        return getattr(self, attr_name)

    def unpack_event(self, *args, **kwargs) -> Optional[Union[Exception, bool]]:
        """
        解包事件,解包后对原始数据的重新处理
        """
        return True

    def __init__(self, *args, **kwargs):
        names = set()
        for name, value in zip(self.__data__, args):
            setattr(self, name, value)
            names.add(name)

        for name, value in kwargs.items():
            if name in names:
                raise ValueError(f'Duplicate name: {name}')
            setattr(self, name, value)

        self.serializer_funcs = {
            'pack': pack_attr,
            'unpack': unpack_attr
        }


    @classmethod
    def to_struct(cls, obj, __data__=None):
        """
        根据传入的对象以及__data__列表,构建结构体
        """
        if isinstance(obj, BinStructBase):
            if __data__ is None:
                return obj
            elif __data__ == obj.__data__:
                return obj
            else:
                raise GeneraterError('无法确定结构体需要包含的属性')
        if __data__ is None:
            if hasattr(obj, '__data__'):
                __data__ = getattr(obj, '__data__')

        if __data__ is None:
            raise GeneraterError('无法确定结构体需要包含的属性')

        ins = cls(**{name: getattr(obj, name) for name in __data__})
        ins.__data__ = __data__
        return ins

    @classmethod
    def is_registered(cls):
        """
        检查此类是否已经注册
        """
        return get_qualname(cls) in bin_types

    @property
    def __attrs_dict(self):
        dct = {}
        for name in self.__data__:
            dct[name] = getattr(self, name)
        return dct

    def __str__(self):
        kv_pairs = list(self.__attrs_dict.items())
        return f'{self.__class__.__name__}({", ".join((f"{name}={repr(value)}" for name, value in kv_pairs))})'

    def __eq__(self, other):
        if not isinstance(other, BinStructBase):
            return False
        return self.__attrs_dict == other.__attrs_dict

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(tuple(self.__attrs_dict.items()))

    __repr__ = __str__


class Struct(abc.Serializer):
    struct = BinStructBase

    def dumps(self, data: Union[BinStructBase, typing.Any]):
        if isinstance(data, self.struct):
            return data.pack()
        else:
            return self.struct.mini_pack(data)

    def loads(self, data, __data__=None, mini=False):
        if mini is True:
            return self.struct.mini_unpack(data)
        elif mini is False:
            return self.struct.unpack(data, __data__=__data__)
        else:
            try:
                return self.struct.unpack(data, __data__=__data__)
            except:
                return self.struct.mini_unpack(data)


bin_types = {
    get_qualname(BinStructBase),
}

_flush_lock = Lock()


def flush_bin_types():
    """
    为了保证自定义的BinStruct子类能被正确解析,需要调用此函数刷新结构体注册表
    """
    with _flush_lock:
        global bin_types
        bin_types |= set((get_qualname(cls) for cls in get_subclasses_recursion(BinStructBase)))


def get_bin_types():
    return bin_types.copy()
