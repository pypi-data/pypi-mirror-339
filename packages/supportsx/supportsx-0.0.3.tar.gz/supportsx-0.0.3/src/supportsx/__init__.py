"""A Python library that supplies runtime-checkable, fully
parameterized, and well-documented protocols for nearly all dunder
methods/attributes.

Example (direct access):
```
from typing import Any
import supportsx

def foo(
    value: supportsx.add[Any, int],
    ctm: supportsx.u.ctx_mngr
) -> None:
    with ctm:
        print(value + 1)
```

Example (import from):
```
from typing import Any
from supportsx import *

def foo(
    value: SupportsAdd[Any, int],
    ctm: SupportsContextManager
) -> None:
    with ctm:
        print(value + 1)
```

:copyright: (c) 2024 Tanner Corcoran
:license: Apache 2.0, see LICENSE for more details.

"""

__title__ = "supportsx"
__author__ = "Tanner Corcoran"
__email__ = "tannerbcorcoran@gmail.com"
__license__ = "Apache 2.0 License"
__copyright__ = "Copyright (c) 2024 Tanner Corcoran"
__version__ = "0.0.3"
__description__ = (
    "A Python library that supplies runtime-checkable, fully parameterized,"
    " and well-documented protocols for nearly all dunder methods/attributes."
)
__url__ = "https://github.com/tanrbobanr/supportsx"
__download_url__ = "https://pypi.org/project/supportsx"


from ._supports import *
from ._supports import (
    SupportsAbs as abs,
    SupportsAdd as add,
    SupportsAEnter as aenter,
    SupportsAExit as aexit,
    SupportsAIter as aiter,
    SupportsAnd as and_,
    SupportsANext as anext,
    SupportsAwait as await_,
    SupportsBool as bool,
    SupportsBuffer as buffer,
    SupportsBytes as bytes,
    SupportsCall as call,
    SupportsCeil as ceil,
    SupportsComplex as complex,
    SupportsContains as contains,
    SupportsDelete as delete,
    SupportsDelItem as delitem,
    SupportsDivMod as divmod,
    SupportsEnter as enter,
    SupportsExit as exit,
    SupportsFloat as float,
    SupportsFloor as floor,
    SupportsFloorDiv as floordiv,
    SupportsGE as ge,
    SupportsGet as get,
    SupportsGetAttr as getattr,
    SupportsGetItem as getitem,
    SupportsGT as gt,
    SupportsIAdd as iadd,
    SupportsIAnd as iand,
    SupportsIFloorDiv as ifloordiv,
    SupportsILShift as ilshift,
    SupportsIMatMul as imatmul,
    SupportsIMod as imod,
    SupportsIMul as imul,
    SupportsIndex as index,
    SupportsInt as int,
    SupportsInvert as invert,
    SupportsIOr as ior,
    SupportsIPow as ipow,
    SupportsIRShift as irshift,
    SupportsISub as isub,
    SupportsIter as iter,
    SupportsITrueDiv as itruediv,
    SupportsIXor as ixor,
    SupportsLE as le,
    SupportsLen as len,
    SupportsLengthHint as length_hint,
    SupportsLShift as lshift,
    SupportsLT as lt,
    SupportsMatchArgs as match_args,
    SupportsMatMul as matmul,
    SupportsMissing as missing,
    SupportsMod as mod,
    SupportsMroEntries as mro_entries,
    SupportsMul as mul,
    SupportsNeg as neg,
    SupportsNext as next,
    SupportsObjClass as objclass,
    SupportsOr as or_,
    SupportsPos as pos,
    SupportsPostInit as post_init,
    SupportsPow as pow,
    SupportsRAdd as radd,
    SupportsRAnd as rand,
    SupportsRDivMod as rdivmod,
    SupportsReleaseBuffer as release_buffer,
    SupportsReversed as reversed,
    SupportsRFloorDiv as rfloordiv,
    SupportsRLShift as rlshift,
    SupportsRMatMul as rmatmul,
    SupportsRMod as rmod,
    SupportsRMul as rmul,
    SupportsROr as ror,
    SupportsRound as round,
    SupportsRPow as rpow,
    SupportsRRShift as rrshift,
    SupportsRShift as rshift,
    SupportsRSub as rsub,
    SupportsRTrueDiv as rtruediv,
    SupportsRXor as rxor,
    SupportsSet as set,
    SupportsSetItem as setitem,
    SupportsSetName as set_name,
    SupportsSub as sub,
    SupportsTrueDiv as truediv,
    SupportsTrunc as trunc,
    SupportsXor as xor,
)
from .u import *
from . import u


__all__ = (
    # _supports
    "SupportsAbs",
    "SupportsAdd",
    "SupportsAEnter",
    "SupportsAExit",
    "SupportsAIter",
    "SupportsAnd",
    "SupportsANext",
    "SupportsAwait",
    "SupportsBool",
    "SupportsBuffer",
    "SupportsBytes",
    "SupportsCall",
    "SupportsCeil",
    "SupportsComplex",
    "SupportsContains",
    "SupportsDelete",
    "SupportsDelItem",
    "SupportsDivMod",
    "SupportsEnter",
    "SupportsExit",
    "SupportsFloat",
    "SupportsFloor",
    "SupportsFloorDiv",
    "SupportsGE",
    "SupportsGet",
    "SupportsGetAttr",
    "SupportsGetItem",
    "SupportsGT",
    "SupportsIAdd",
    "SupportsIAnd",
    "SupportsIFloorDiv",
    "SupportsILShift",
    "SupportsIMatMul",
    "SupportsIMod",
    "SupportsIMul",
    "SupportsIndex",
    "SupportsInt",
    "SupportsInvert",
    "SupportsIOr",
    "SupportsIPow",
    "SupportsIRShift",
    "SupportsISub",
    "SupportsIter",
    "SupportsITrueDiv",
    "SupportsIXor",
    "SupportsLE",
    "SupportsLen",
    "SupportsLengthHint",
    "SupportsLShift",
    "SupportsLT",
    "SupportsMatchArgs",
    "SupportsMatMul",
    "SupportsMissing",
    "SupportsMod",
    "SupportsMroEntries",
    "SupportsMul",
    "SupportsNeg",
    "SupportsNext",
    "SupportsObjClass",
    "SupportsOr",
    "SupportsPos",
    "SupportsPostInit",
    "SupportsPow",
    "SupportsRAdd",
    "SupportsRAnd",
    "SupportsRDivMod",
    "SupportsReleaseBuffer",
    "SupportsReversed",
    "SupportsRFloorDiv",
    "SupportsRLShift",
    "SupportsRMatMul",
    "SupportsRMod",
    "SupportsRMul",
    "SupportsROr",
    "SupportsRound",
    "SupportsRPow",
    "SupportsRRShift",
    "SupportsRShift",
    "SupportsRSub",
    "SupportsRTrueDiv",
    "SupportsRXor",
    "SupportsSet",
    "SupportsSetItem",
    "SupportsSetName",
    "SupportsSub",
    "SupportsTrueDiv",
    "SupportsTrunc",
    "SupportsXor",

    # _unions
    "SupportsAsyncContextManager",
    "SupportsBitwiseOps",
    "SupportsComparisons",
    "SupportsContextManager",
    "SupportsDataDescriptor",
    "SupportsIBitwiseOps",
    "SupportsIMathOps",
    "SupportsIMathOps2",
    "SupportsItems",
    "SupportsLength",
    "SupportsMathFunctions",
    "SupportsMathOps",
    "SupportsMathOps2",
    "SupportsTypeConversion",
    "SupportsTypeConversion2",
    "SupportsUnaryOps",
)
