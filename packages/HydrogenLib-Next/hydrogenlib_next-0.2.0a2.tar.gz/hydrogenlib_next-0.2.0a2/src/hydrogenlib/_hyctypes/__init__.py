"""
Use:
    from ctypes import c_int
    dll = HyDll(<dll_name>, STDCALL | C)

    @dll.function
    def AnyFunction(a: c_int, b: c_int) -> None: ...

    @dll.function
    def ... ( ... ) -> ... : ...
"""

from ctypes import *
from ctypes import util

from .dll import HyDll, CDECL, STDCALL
from .universality import HyStructure


import os as _os

if _os.name == 'nt':
    from ctypes.wintypes import *

from .methods import *
