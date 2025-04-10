"""All union `Supports*` protocols.

:copyright: (c) 2024 Tanner Corcoran
:license: Apache 2.0, see LICENSE for more details.

"""

__author__ = "Tanner Corcoran"
__license__ = "Apache 2.0 License"
__copyright__ = "Copyright (c) 2024 Tanner Corcoran"


from ._unions import *
from ._unions import (
    SupportsAsyncContextManager as actx_mngr,
    SupportsBitwiseOps as bitops,
    SupportsComparisons as cmps,
    SupportsContextManager as ctx_mngr,
    SupportsDataDescriptor as data_desc,
    SupportsIBitwiseOps as ibitops,
    SupportsIMathOps as imathops,
    SupportsIMathOps2 as imathops2,
    SupportsItems as items,
    SupportsLength as length,
    SupportsMathFunctions as math_funcs,
    SupportsMathOps as mathops,
    SupportsMathOps2 as mathops2,
    SupportsTypeConversion as type_conversion,
    SupportsTypeConversion2 as type_conversion2,
    SupportsUnaryOps as unary_ops,
)


__all__ = (
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
