"""Definitions for all union `Supports*` protocols.

:copyright: (c) 2024 Tanner Corcoran
:license: Apache 2.0, see LICENSE for more details.

"""

__author__ = "Tanner Corcoran"
__license__ = "Apache 2.0 License"
__copyright__ = "Copyright (c) 2024 Tanner Corcoran"


from typing import (
    Protocol,
    TypeVar,
    runtime_checkable,
)

from .._supports import (
    SupportsAbs,
    SupportsAdd,
    SupportsAEnter,
    SupportsAExit,
    SupportsAnd,
    SupportsBool,
    SupportsBytes,
    SupportsCeil,
    SupportsComplex,
    SupportsDelete,
    SupportsDelItem,
    SupportsDivMod,
    SupportsEnter,
    SupportsExit,
    SupportsFloat,
    SupportsFloor,
    SupportsFloorDiv,
    SupportsGE,
    SupportsGet,
    SupportsGetItem,
    SupportsGT,
    SupportsIAdd,
    SupportsIAnd,
    SupportsIFloorDiv,
    SupportsILShift,
    SupportsIMatMul,
    SupportsIMod,
    SupportsIMul,
    SupportsIndex,
    SupportsInt,
    SupportsInvert,
    SupportsIOr,
    SupportsIPow,
    SupportsIRShift,
    SupportsISub,
    SupportsITrueDiv,
    SupportsIXor,
    SupportsLE,
    SupportsLen,
    SupportsLengthHint,
    SupportsLShift,
    SupportsLT,
    SupportsMatMul,
    SupportsMod,
    SupportsMul,
    SupportsNeg,
    SupportsOr,
    SupportsPos,
    SupportsPow,
    SupportsRAdd,
    SupportsRAnd,
    SupportsRDivMod,
    SupportsRFloorDiv,
    SupportsRLShift,
    SupportsRMatMul,
    SupportsRMod,
    SupportsRMul,
    SupportsROr,
    SupportsRound,
    SupportsRPow,
    SupportsRRShift,
    SupportsRShift,
    SupportsRSub,
    SupportsRTrueDiv,
    SupportsRXor,
    SupportsSet,
    SupportsSetItem,
    SupportsSub,
    SupportsTrueDiv,
    SupportsTrunc,
    SupportsXor,
)


_T_co = TypeVar("_T_co", covariant=True)
_T2_co = TypeVar("_T2_co", covariant=True)
_T3_co = TypeVar("_T3_co", covariant=True)
_T4_co = TypeVar("_T4_co", covariant=True)
_T_contra = TypeVar("_T_contra", contravariant=True)
_T2_contra = TypeVar("_T2_contra", contravariant=True)


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


@runtime_checkable
class SupportsAsyncContextManager(
    SupportsAEnter[_T_co], SupportsAExit, Protocol[_T_co]
):
    """Async context manager (i.e. defines both `__aenter__` and
    `__aexit__`).

    A protocol `[_T_co]` that is a union of:
    - `SupportsAEnter[_T_co]`
    - `SupportsAExit`

    """


@runtime_checkable
class SupportsBitwiseOps(
    SupportsAnd[_T_contra, _T_co],
    SupportsLShift[_T_contra, _T_co],
    SupportsOr[_T_contra, _T_co],
    SupportsRAnd[_T_contra, _T_co],
    SupportsRLShift[_T_contra, _T_co],
    SupportsROr[_T_contra, _T_co],
    SupportsRRShift[_T_contra, _T_co],
    SupportsRShift[_T_contra, _T_co],
    SupportsRXor[_T_contra, _T_co],
    SupportsXor[_T_contra, _T_co],
    Protocol[_T_contra, _T_co]
):
    """The bitwise operators: `&`, `<<`, `|`, `>>`, and `^`.

    A protocol `[_T_contra, _T_co]` that is a union of:
    - `SupportsAnd[_T_contra, _T_co]`
    - `SupportsLShift[_T_contra, _T_co]`
    - `SupportsOr[_T_contra, _T_co]`
    - `SupportsRAnd[_T_contra, _T_co]`
    - `SupportsRLShift[_T_contra, _T_co]`
    - `SupportsROr[_T_contra, _T_co]`
    - `SupportsRRShift[_T_contra, _T_co]`
    - `SupportsRShift[_T_contra, _T_co]`
    - `SupportsRXor[_T_contra, _T_co]`
    - `SupportsXor[_T_contra, _T_co]`

    """


@runtime_checkable
class SupportsComparisons(
    SupportsGE[_T_contra],
    SupportsGT[_T_contra],
    SupportsLE[_T_contra],
    SupportsLT[_T_contra],
    Protocol[_T_contra]
):
    """Comparisons operators: `>=`, `>`, `<=`, and `<`.

    A protocol `[_T_contra]` that is a union of:
    - `SupportsGE[_T_contra]`
    - `SupportsGT[_T_contra]`
    - `SupportsLE[_T_contra]`
    - `SupportsLT[_T_contra]`

    """


@runtime_checkable
class SupportsContextManager(
    SupportsEnter[_T_co], SupportsExit, Protocol[_T_co]
):
    """Context manager (i.e. defines both `__enter__` and `__exit__`).

    A protocol `[_T_co]` that is a union of:
    - `SupportsEnter[_T_co]`
    - `SupportsExit`

    """


@runtime_checkable
class SupportsDataDescriptor(
    SupportsDelete[_T_contra],
    SupportsGet[_T_contra, _T_co],
    SupportsSet[_T_contra, _T2_contra],
    Protocol[_T_contra, _T2_contra, _T_co]
):
    """Something that supports the descriptor protocol (i.e. defines
    `__delete__`, `__get__`, and `__set__`).

    A protocol `[_T_contra, _T2_contra, _T_co]` that is a union of:
    - `SupportsDelete[_T_contra]`
    - `SupportsGet[_T_contra, _T_co]`
    - `SupportsSet[_T_contra, _T2_contra]`

    """


@runtime_checkable
class SupportsIBitwiseOps(
    SupportsIAnd[_T_contra],
    SupportsILShift[_T_contra],
    SupportsIOr[_T_contra],
    SupportsIRShift[_T_contra],
    SupportsIXor[_T_contra],
    Protocol[_T_contra]
):
    """The in-place bitwise operators: `&=`, `<<=`, `|=`, `>>=`, and
    `^=`.

    A protocol `[_T_contra]` that is a union of:
    - `SupportsIAnd[_T_contra]`
    - `SupportsILShift[_T_contra]`
    - `SupportsIOr[_T_contra]`
    - `SupportsIRShift[_T_contra]`
    - `SupportsIXor[_T_contra]`

    """


@runtime_checkable
class SupportsIMathOps(
    SupportsIAdd[_T_contra],
    SupportsIFloorDiv[_T_contra],
    SupportsIMod[_T_contra],
    SupportsIMul[_T_contra],
    SupportsIPow[_T_contra, _T2_contra],
    SupportsISub[_T_contra],
    SupportsITrueDiv[_T_contra],
    Protocol[_T_contra, _T2_contra]
):
    """The in-place math operators: `+=`, `//=`, `%=`, `*=`, `**=`,
    `-=`, and `/=`.

    A protocol `[_T_contra, _T2_contra]` that is a union of:
    - `SupportsIAdd[_T_contra]`
    - `SupportsIFloorDiv[_T_contra]`
    - `SupportsIMod[_T_contra]`
    - `SupportsIMul[_T_contra]`
    - `SupportsIPow[_T_contra, _T2_contra]`
    - `SupportsISub[_T_contra]`
    - `SupportsITrueDiv[_T_contra]`

    Note: The matmul (`@`) is not included as it is not used in builtin
    functions (e.g. `int`, `float`, etc.). If you need matmul as well,
    use `SupportsIMathOps2`.

    """


@runtime_checkable
class SupportsIMathOps2(
    SupportsIMathOps[_T_contra, _T2_contra],
    SupportsIMatMul[_T_contra],
    Protocol[_T_contra, _T2_contra]
):
    """The in-place math operators along with `@=`.

    A protocol `[_T_contra, _T2_contra]` that is a union of:
    - `SupportsIMathOps[_T_contra, _T2_contra]`
    - `SupportsIMatMul[_T_contra]`

    """


@runtime_checkable
class SupportsItems(
    SupportsDelItem[_T_contra],
    SupportsGetItem[_T_contra, _T_co],
    SupportsSetItem[_T_contra, _T2_contra],
    Protocol[_T_contra, _T2_contra, _T_co]
):
    """Something that supports the subscription methods (i.e. defines
    `__delitem__`, `__getitem__`, and `__setitem__`).

    A protocol `[_T_contra, _T2_contra, _T_co]` that is a union of:
    - `SupportsDelItem[_T_contra]`
    - `SupportsGetItem[_T_contra, _T_co]`
    - `SupportsSetItem[_T_contra, _T2_contra]`

    """


@runtime_checkable
class SupportsLength(
    SupportsLen,
    SupportsLengthHint,
    Protocol
):
    """Something that has full length support (i.e. defines both
    `__len__` and `__length_hint__`).

    A protocol that is a union of:
    - `SupportsLen`
    - `SupportsLengthHint`

    """


@runtime_checkable
class SupportsMathFunctions(
    SupportsAbs[_T2_co],
    SupportsCeil,
    SupportsDivMod[_T_contra, _T_co],
    SupportsFloor,
    SupportsRDivMod[_T_contra, _T_co],
    SupportsRound[_T3_co, _T4_co],
    SupportsTrunc,
    Protocol[_T_contra, _T_co, _T2_co, _T3_co, _T4_co]
):
    """The math functions: `abs()`, `math.ceil()`, `divmod()`,
    `math.floor()`, `round()`, `math.trunc()`.

    A protocol `[_T_contra, _T_co, _T2_co, _T3_co, _T4_co]` that is a union of:
    - `SupportsAbs[_T2_co]`
    - `SupportsCeil`
    - `SupportsDivMod[_T_contra, _T_co]`
    - `SupportsFloor`
    - `SupportsRDivMod[_T_contra, _T_co]`
    - `SupportsRound[_T3_co, _T4_co]`
    - `SupportsTrunc`

    """


@runtime_checkable
class SupportsMathOps(
    SupportsAdd[_T_contra, _T_co],
    SupportsFloorDiv[_T_contra, _T_co],
    SupportsMod[_T_contra, _T_co],
    SupportsMul[_T_contra, _T_co],
    SupportsPow[_T_contra, _T2_contra, _T_co],
    SupportsRAdd[_T_contra, _T_co],
    SupportsRFloorDiv[_T_contra, _T_co],
    SupportsRMod[_T_contra, _T_co],
    SupportsRMul[_T_contra, _T_co],
    SupportsRPow[_T_contra, _T2_contra, _T_co],
    SupportsRSub[_T_contra, _T_co],
    SupportsRTrueDiv[_T_contra, _T_co],
    SupportsSub[_T_contra, _T_co],
    SupportsTrueDiv[_T_contra, _T_co],
    Protocol[_T_contra, _T2_contra, _T_co]
):
    """The math operators: `+`, `//`, `%`, `*`, `**`, `-`, and `/`.

    A protocol `[_T_contra, _T2_contra, _T_co]` that is a union of:
    - `SupportsAdd[_T_contra, _T_co]`
    - `SupportsFloorDiv[_T_contra, _T_co]`
    - `SupportsMod[_T_contra, _T_co]`
    - `SupportsMul[_T_contra, _T_co]`
    - `SupportsPow[_T_contra, _T2_contra, _T_co]`
    - `SupportsRAdd[_T_contra, _T_co]`
    - `SupportsRFloorDiv[_T_contra, _T_co]`
    - `SupportsRMod[_T_contra, _T_co]`
    - `SupportsRMul[_T_contra, _T_co]`
    - `SupportsRPow[_T_contra, _T2_contra, _T_co]`
    - `SupportsRSub[_T_contra, _T_co]`
    - `SupportsRTrueDiv[_T_contra, _T_co]`
    - `SupportsSub[_T_contra, _T_co]`
    - `SupportsTrueDiv[_T_contra, _T_co]`

    Note: The matmul (`@`) is not included as it is not used in builtin
    functions (e.g. `int`, `float`, etc.). If you need matmul as well,
    use `SupportsMathOps2`.

    """


@runtime_checkable
class SupportsMathOps2(
    SupportsMathOps[_T_contra, _T2_contra, _T_co],
    SupportsMatMul[_T_contra, _T_co],
    SupportsRMatMul[_T_contra, _T_co],
    Protocol[_T_contra, _T2_contra, _T_co]
):
    """The math operators along with `@`.

    A protocol `[_T_contra, _T2_contra, _T_co]` that is a union of:
    - `SupportsMathOps[_T_contra, _T2_contra, _T_co]`
    - `SupportsMatMul[_T_contra, _T_co]`
    - `SupportsRMatMul[_T_contra, _T_co]`

    """


@runtime_checkable
class SupportsTypeConversion(
    SupportsBytes,
    SupportsComplex,
    SupportsFloat,
    SupportsIndex,
    SupportsInt,
    Protocol
):
    """Type conversions: `bytes()`, `complex()`, `float()`, `int()`, as
    well as implicit integer type coercion via `__index__`.

    A protocol that is a union of:
    - `SupportsBytes`
    - `SupportsComplex`
    - `SupportsFloat`
    - `SupportsIndex`
    - `SupportsInt`

    Note: Because `__bool__` as additional uses other than type
    conversion via `bool()`, it is not included in this union type. If
    you need `__bool__` as well, use `SupportsTypeConversions2`.

    """


@runtime_checkable
class SupportsTypeConversion2(
    SupportsBool,
    SupportsTypeConversion,
    Protocol
):
    """Type conversions along with `bool()`.

    A protocol that is a union of:
    - `SupportsTypeConversion`
    - `SupportsBool`

    """


@runtime_checkable
class SupportsUnaryOps(
    SupportsInvert[_T_co],
    SupportsNeg[_T_co],
    SupportsPos[_T_co],
    Protocol[_T_co]
):
    """The unary operators: `~`, `-`, and `+`.

    A protocol `[_T_co]` that is a union of:
    - `SupportsInvert[_T_co]`
    - `SupportsNeg[_T_co]`
    - `SupportsPos[_T_co]`

    """
