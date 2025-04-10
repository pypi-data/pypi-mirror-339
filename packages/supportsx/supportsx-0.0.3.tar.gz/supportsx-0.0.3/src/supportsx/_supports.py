"""Definitions for all primary `Supports*` protocols.

:copyright: (c) 2024 Tanner Corcoran
:license: Apache 2.0, see LICENSE for more details.

"""

__author__ = "Tanner Corcoran"
__license__ = "Apache 2.0 License"
__copyright__ = "Copyright (c) 2024 Tanner Corcoran"


import sys
import abc
from collections.abc import (
    AsyncIterator,
    Awaitable,
    Iterator,
    Sequence,
)
from typing import (
    Protocol,
    TypeVar,
    Union,
    runtime_checkable,
    overload,
)
if sys.version_info >= (3, 10):
    from typing import ParamSpec
else:
    from typing_extensions import ParamSpec
from types import TracebackType


_T = TypeVar("_T")
_T_co = TypeVar("_T_co", covariant=True)
_T2_co = TypeVar("_T2_co", covariant=True)
_T_contra = TypeVar("_T_contra", contravariant=True)
_T2_contra = TypeVar("_T2_contra", contravariant=True)
_P = ParamSpec("_P")


__all__ = (
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
)


# List of ignored methods:
# - __delattr__ (all types/objects)
# - __dir__ (all types/objects)
# - __eq__ (all types/objects)
# - __format__ (all types/objects)
# - __getattribute__ (all types/objects)
# - __getstate__ (all types/objects)
# - __hash__ (all types/objects)
# - __init__ (all types/objects)
# - __init_subclass__ (all types/objects)
# - __instancecheck__ (all types)
# - __ne__ (all types/objects)
# - __new__ (all types/objects)
# - __prepare__ (all types)
# - __reduce__ (all types/objects)
# - __reduce_ex__ (all types/objects)
# - __repr__ (all types/objects)
# - __setattr__ (all types/objects)
# - __sizeof__ (all types/objects)
# - __str__ (all types/objects)
# - __subclasscheck__ (all types)
# - __subclasses__ (all types)
# - __subclasshook__ (all types/objects)
# - mro (all types)

# List of ignored attributes:
# - __base__ (all types)
# - __bases__ (all types)
# - __basicsize__ (all types)
# - __class__ (all types)
# - __dictoffset__ (all types)
# - __flags__ (all types)
# - __itemsize__ (all types)
# - __module__ (all types)
# - __mro__ (all types)
# - __name__ (all types)
# - __qualname__ (all types)
# - __text_signature__ (all types)
# - __type_params__ (all types)
# - __weakrefoffset__ (all types)

# Additional ignores:
# - __slots__ and __dict__ don't currently support type hints


@runtime_checkable
class SupportsAbs(Protocol[_T_co]):
    """A protocol `[_T_co]` with one abstract method `__abs__` of the
    form `() -> _T_co`.

    """

    __slots__ = ()

    @abc.abstractmethod
    def __abs__(self) -> _T_co:
        pass


@runtime_checkable
class SupportsAdd(Protocol[_T_contra, _T_co]):
    """A protocol `[_T_contra, _T_co]` with one abstract method
    `__add__` of the form `(_T_contra) -> _T_co`.

    """

    __slots__ = ()

    @abc.abstractmethod
    def __add__(self, other: _T_contra, /) -> _T_co:
        pass


@runtime_checkable
class SupportsAEnter(Protocol[_T_co]):
    """A protocol `[_T_co]` with one abstract method `__aenter__` of the
    form `() -> Awaitable[_T_co]`.

    """

    __slots__ = ()

    @abc.abstractmethod
    def __aenter__(self) -> Awaitable[_T_co]:
        pass


@runtime_checkable
class SupportsAExit(Protocol):
    """A protocol with one abstract method `__aexit__` of the form
    `(Type[BaseException] | None, BaseException | None,
    TracebackType | None) -> Awaitable[None]`.

    """

    __slots__ = ()

    @abc.abstractmethod
    def __aexit__(
        self, exc_type: Union[type[BaseException], None],
        exc_val: Union[BaseException, None],
        exc_tb: Union[TracebackType, None], /
    ) -> Awaitable[None]:
        pass


@runtime_checkable
class SupportsAIter(Protocol[_T_co]):
    """A protocol `[_T_co]` with one abstract method `__aiter__` of the
    form `() -> AsyncIterator[_T_co]`.

    """

    __slots__ = ()

    @abc.abstractmethod
    def __aiter__(self) -> AsyncIterator[_T_co]:
        pass


@runtime_checkable
class SupportsAnd(Protocol[_T_contra, _T_co]):
    """A protocol `[_T_contra, _T_co]` with one abstract method
    `__and__` of the form `(_T_contra) -> _T_co`.

    """

    __slots__ = ()

    @abc.abstractmethod
    def __and__(self, other: _T_contra, /) -> _T_co:
        pass


@runtime_checkable
class SupportsANext(Protocol[_T_co]):
    """A protocol `[_T_co]` with one abstract method `__anext__` of the
    form `() -> Awaitable[_T_co]`.

    """

    __slots__ = ()

    @abc.abstractmethod
    def __anext__(self) -> Awaitable[_T_co]:
        pass


@runtime_checkable
class SupportsAwait(Protocol[_T_co]):
    """A protocol `[_T_co]` with one abstract method `__await__` of the
    form `() -> Iterator[_T_co]`.

    """

    __slots__ = ()

    @abc.abstractmethod
    def __await__(self) -> Iterator[_T_co]:
        pass


@runtime_checkable
class SupportsBool(Protocol):
    """A protocol with one abstract method `__bool__` of the form
    `() -> bool`.

    """

    __slots__ = ()

    @abc.abstractmethod
    def __bool__(self) -> bool:
        pass


@runtime_checkable
class SupportsBuffer(Protocol):
    """A protocol with one abstract method `__buffer__` of the form
    `(int) -> memoryview`.

    """

    __slots__ = ()

    @abc.abstractmethod
    def __buffer__(self, flags: int, /) -> memoryview:
        pass


@runtime_checkable
class SupportsBytes(Protocol):
    """A protocol with one abstract method `__bytes__` of the form
    `() -> bytes`.

    """

    __slots__ = ()

    @abc.abstractmethod
    def __bytes__(self) -> bytes:
        pass


@runtime_checkable
class SupportsCall(Protocol[_P, _T_co]):
    """A protocol `[_P, _T_co]` with one abstract method `__call__` of
    the form `(_P) -> _T_co`.

    """

    __slots__ = ()

    @abc.abstractmethod
    def __call__(self, *args: _P.args, **kwargs: _P.kwargs) -> _T_co:
        pass


@runtime_checkable
class SupportsCeil(Protocol):
    """A protocol with one abstract method `__ceil__` of the form
    `() -> Integral`.

    """

    __slots__ = ()

    @abc.abstractmethod
    def __ceil__(self) -> int:
        pass


@runtime_checkable
class SupportsComplex(Protocol):
    """A protocol with one abstract method `__complex__` of the form
    `() -> complex`.

    """

    __slots__ = ()

    @abc.abstractmethod
    def __complex__(self) -> complex:
        pass


@runtime_checkable
class SupportsContains(Protocol[_T_contra]):
    """A protocol `[_T_contra]` with one abstract method `__contains__`
    of the form `(_T_contra) -> bool`.

    """

    __slots__ = ()

    @abc.abstractmethod
    def __contains__(self, value: _T_contra, /) -> bool:
        pass


@runtime_checkable
class SupportsDelete(Protocol[_T_contra]):
    """A protocol `[_T_contra]` with one abstract method `__delete__` of
    the form `(_T_contra) -> None`.

    """

    __slots__ = ()

    @abc.abstractmethod
    def __delete__(self, instance: _T_contra) -> None:
        pass


@runtime_checkable
class SupportsDelItem(Protocol[_T_contra]):
    """A protocol `[_T_contra]` with one abstract method `__delitem__`
    of the form `(_T_contra) -> None`.

    """

    __slots__ = ()

    @abc.abstractmethod
    def __delitem__(self, key: _T_contra, /) -> None:
        pass


@runtime_checkable
class SupportsDivMod(Protocol[_T_contra, _T_co]):
    """A protocol `[_T_contra, _T_co]` with one abstract method
    `__divmod__` of the form `(_T_contra) -> _T_co`.

    """

    __slots__ = ()

    @abc.abstractmethod
    def __divmod__(self, other: _T_contra, /) -> _T_co:
        pass


@runtime_checkable
class SupportsEnter(Protocol[_T_co]):
    """A protocol `[_T_co]` with one abstract method `__enter__` of the
    form `() -> _T_co`.

    """

    __slots__ = ()

    @abc.abstractmethod
    def __enter__(self) -> _T_co:
        pass


@runtime_checkable
class SupportsExit(Protocol):
    """A protocol with one abstract method `__exit__` of the form
    `(Type[BaseException] | None, BaseException | None,
    TracebackType | None) -> None`.

    """

    __slots__ = ()

    @abc.abstractmethod
    def __exit__(
        self, exc_type: Union[type[BaseException], None],
        exc_val: Union[type[BaseException], None],
        exc_tb: Union[TracebackType, None], /
    ) -> None:
        pass


@runtime_checkable
class SupportsFloat(Protocol):
    """A protocol with one abstract method `__float__` of the form
    `() -> float`.

    """

    __slots__ = ()

    @abc.abstractmethod
    def __float__(self) -> float:
        pass


@runtime_checkable
class SupportsFloor(Protocol):
    """A protocol with one abstract method `__floor__` of the form
    `() -> Integral`.

    """

    __slots__ = ()

    @abc.abstractmethod
    def __floor__(self) -> int:
        pass


@runtime_checkable
class SupportsFloorDiv(Protocol[_T_contra, _T_co]):
    """A protocol `[_T_contra, _T_co]` with one abstract method
    `__floordiv__` of the form `(_T_contra) -> _T_co`.

    """

    __slots__ = ()

    @abc.abstractmethod
    def __floordiv__(self, other: _T_contra, /) -> _T_co:
        pass


@runtime_checkable
class SupportsGE(Protocol[_T_contra]):
    """A protocol `[_T_contra]` with one abstract method `__ge__` of the
    form `(_T_contra) -> bool`.

    """

    __slots__ = ()

    @abc.abstractmethod
    def __ge__(self, other: _T_contra, /) -> bool:
        pass


@runtime_checkable
class SupportsGet(Protocol[_T_contra, _T_co]):
    """A protocol `[_T_contra, _T_co]` with one abstract method
    `__get__` of the form
    `(_T_contra | None, Type[_T_contra] | None = None) -> _T_co`.

    """

    __slots__ = ()

    @abc.abstractmethod
    def __get__(
        self, instance: Union[_T_contra, None],
        owner: Union[type[_T_contra], None] = None
    ) -> _T_co:
        pass


@runtime_checkable
class SupportsGetAttr(Protocol[_T_co]):
    """A protocol `[_T_co]` with one abstract method `__getattr__` of
    the form `(str) -> _T_co`.

    """

    __slots__ = ()

    @abc.abstractmethod
    def __getattr__(self, name: str, /) -> _T_co:
        pass


@runtime_checkable
class SupportsGetItem(Protocol[_T_contra, _T_co]):
    """A protocol `[_T_contra, _T_co]` with one abstract method
    `__getitem__` of the form `(_T_contra) -> _T_co`.

    """

    __slots__ = ()

    @abc.abstractmethod
    def __getitem__(self, key: _T_contra, /) -> _T_co:
        pass


@runtime_checkable
class SupportsGT(Protocol[_T_contra]):
    """A protocol `[_T_contra]` with one abstract method `__gt__` of the
    form `(_T_contra) -> bool`.

    """

    __slots__ = ()

    @abc.abstractmethod
    def __gt__(self, other: _T_contra, /) -> bool:
        pass


@runtime_checkable
class SupportsIAdd(Protocol[_T_contra]):
    """A protocol `[_T_contra]` with one abstract method `__iadd__` of
    the form `(_T_contra) -> None`.

    """

    __slots__ = ()

    @abc.abstractmethod
    def __iadd__(self, other: _T_contra, /) -> None:
        pass


@runtime_checkable
class SupportsIAnd(Protocol[_T_contra]):
    """A protocol `[_T_contra]` with one abstract method `__iand__` of
    the form `(_T_contra) -> None`.

    """

    __slots__ = ()

    @abc.abstractmethod
    def __iand__(self, other: _T_contra, /) -> None:
        pass


@runtime_checkable
class SupportsIFloorDiv(Protocol[_T_contra]):
    """A protocol `[_T_contra]` with one abstract method `__ifloordiv__`
    of the form `(_T_contra) -> None`.

    """

    __slots__ = ()

    @abc.abstractmethod
    def __ifloordiv__(self, other: _T_contra, /) -> None:
        pass


@runtime_checkable
class SupportsILShift(Protocol[_T_contra]):
    """A protocol `[_T_contra]` with one abstract method `__ilshift__`
    of the form `(_T_contra) -> None`.

    """

    __slots__ = ()

    @abc.abstractmethod
    def __ilshift__(self, other: _T_contra, /) -> None:
        pass


@runtime_checkable
class SupportsIMatMul(Protocol[_T_contra]):
    """A protocol `[_T_contra]` with one abstract method `__imatmul__`
    of the form `(_T_contra) -> None`.

    """

    __slots__ = ()

    @abc.abstractmethod
    def __imatmul__(self, other: _T_contra, /) -> None:
        pass


@runtime_checkable
class SupportsIMod(Protocol[_T_contra]):
    """A protocol `[_T_contra]` with one abstract method `__imod__` of
    the form `(_T_contra) -> None`.

    """

    __slots__ = ()

    @abc.abstractmethod
    def __imod__(self, other: _T_contra, /) -> None:
        pass


@runtime_checkable
class SupportsIMul(Protocol[_T_contra]):
    """A protocol `[_T_contra]` with one abstract method `__imul__` of
    the form `(_T_contra) -> None`.

    """

    __slots__ = ()

    @abc.abstractmethod
    def __imul__(self, other: _T_contra, /) -> None:
        pass


@runtime_checkable
class SupportsIndex(Protocol):
    """A protocol with one abstract method `__index__` of the form
    `() -> int`.

    """

    __slots__ = ()

    @abc.abstractmethod
    def __index__(self) -> int:
        pass


@runtime_checkable
class SupportsInt(Protocol):
    """A protocol with one abstract method `__int__` of the form
    `() -> int`.

    """

    __slots__ = ()

    @abc.abstractmethod
    def __int__(self) -> int:
        pass


@runtime_checkable
class SupportsInvert(Protocol[_T_co]):
    """A protocol `[_T_co]` with one abstract method `__invert__` of the
    form `() -> _T_co`.

    """

    __slots__ = ()

    @abc.abstractmethod
    def __invert__(self) -> _T_co:
        pass


@runtime_checkable
class SupportsIOr(Protocol[_T_contra]):
    """A protocol `[_T_contra]` with one abstract method `__ior__` of
    the form `(_T_contra) -> None`.

    """

    __slots__ = ()

    @abc.abstractmethod
    def __ior__(self, other: _T_contra, /) -> None:
        pass


@runtime_checkable
class SupportsIPow(Protocol[_T_contra, _T2_contra]):
    """A protocol `[_T_contra, _T2_contra]` with one abstract method
    `__ipow__` of the form
    `(_T_contra, _T2_contra | None = None) -> None`.

    """

    __slots__ = ()

    @abc.abstractmethod
    def __ipow__(
        self, other: _T_contra, modulo: Union[_T2_contra, None] = None
    ) -> None:
        pass


@runtime_checkable
class SupportsIRShift(Protocol[_T_contra]):
    """A protocol `[_T_contra]` with one abstract method `__irshift__`
    of the form `(_T_contra) -> None`.

    """

    __slots__ = ()

    @abc.abstractmethod
    def __irshift__(self, other: _T_contra, /) -> None:
        pass


@runtime_checkable
class SupportsISub(Protocol[_T_contra]):
    """A protocol `[_T_contra]` with one abstract method `__isub__` of
    the form `(_T_contra) -> None`.

    """

    __slots__ = ()

    @abc.abstractmethod
    def __isub__(self, other: _T_contra, /) -> None:
        pass


@runtime_checkable
class SupportsIter(Protocol[_T_co]):
    """A protocol `[_T_co]` with one abstract method `__iter__` of the
    form `() -> Iterator[_T_co]`.

    """

    __slots__ = ()

    @abc.abstractmethod
    def __iter__(self) -> Iterator[_T_co]:
        pass


@runtime_checkable
class SupportsITrueDiv(Protocol[_T_contra]):
    """A protocol `[_T_contra]` with one abstract method `__itruediv__`
    of the form `(_T_contra) -> None`.

    """

    __slots__ = ()

    @abc.abstractmethod
    def __itruediv__(self, other: _T_contra, /) -> None:
        pass


@runtime_checkable
class SupportsIXor(Protocol[_T_contra]):
    """A protocol `[_T_contra]` with one abstract method `__ixor__` of
    the form `(_T_contra) -> None`.

    """

    __slots__ = ()

    @abc.abstractmethod
    def __ixor__(self, other: _T_contra, /) -> None:
        pass


@runtime_checkable
class SupportsLE(Protocol[_T_contra]):
    """A protocol `[_T_contra]` with one abstract method `__le__` of the
    form `(_T_contra) -> bool`.

    """

    __slots__ = ()

    @abc.abstractmethod
    def __le__(self, other: _T_contra, /) -> bool:
        pass


@runtime_checkable
class SupportsLen(Protocol):
    """A protocol with one abstract method `__len__` of the form
    `() -> int`.

    """

    __slots__ = ()

    @abc.abstractmethod
    def __len__(self) -> int:
        pass


@runtime_checkable
class SupportsLengthHint(Protocol):
    """A protocol with one abstract method `__length_hint__` of the form
    `() -> int`.

    """

    __slots__ = ()

    @abc.abstractmethod
    def __length_hint__(self) -> int:
        pass


@runtime_checkable
class SupportsLShift(Protocol[_T_contra, _T_co]):
    """A protocol `[_T_contra, _T_co]` with one abstract method
    `__lshift__` of the form `(_T_contra) -> _T_co`.

    """

    __slots__ = ()

    @abc.abstractmethod
    def __lshift__(self, other: _T_contra, /) -> _T_co:
        pass


@runtime_checkable
class SupportsLT(Protocol[_T_contra]):
    """A protocol `[_T_contra]` with one abstract method `__lt__` of the
    form `(_T_contra) -> bool`.

    """

    __slots__ = ()

    @abc.abstractmethod
    def __lt__(self, other: _T_contra, /) -> bool:
        pass


@runtime_checkable
class SupportsMatchArgs(Protocol):
    """A protocol with one abstract property `__match_args__` of the
    form `() -> Sequence[str]`.

    """

    __slots__ = ()

    @property
    @abc.abstractmethod
    def __match_args__(self) -> Sequence[str]:
        pass


@runtime_checkable
class SupportsMatMul(Protocol[_T_contra, _T_co]):
    """A protocol `[_T_contra, _T_co]` with one abstract method
    `__matmul__` of the form `(_T_contra) -> _T_co`.

    """

    __slots__ = ()

    @abc.abstractmethod
    def __matmul__(self, other: _T_contra, /) -> _T_co:
        pass


@runtime_checkable
class SupportsMissing(Protocol[_T_contra, _T_co]):
    """A protocol `[_T_contra, _T_co]` with one abstract method
    `__missing__` of the form `(_T_contra) -> _T_co`.

    """

    __slots__ = ()

    @abc.abstractmethod
    def __missing__(self, key: _T_contra, /) -> _T_co:
        pass


@runtime_checkable
class SupportsMod(Protocol[_T_contra, _T_co]):
    """A protocol `[_T_contra, _T_co]` with one abstract method
    `__mod__` of the form `(_T_contra) -> _T_co`.

    """

    __slots__ = ()

    @abc.abstractmethod
    def __mod__(self, other: _T_contra, /) -> _T_co:
        pass


@runtime_checkable
class SupportsMroEntries(Protocol[_T]):
    """A protocol `[_T]` with one abstract method `__mro_entries__` of
    the form `(Sequence[_T]) -> Sequence[_T]`.

    """

    __slots__ = ()

    @abc.abstractmethod
    def __mro_entries__(self, bases: Sequence[_T], /) -> Sequence[_T]:
        pass


@runtime_checkable
class SupportsMul(Protocol[_T_contra, _T_co]):
    """A protocol `[_T_contra, _T_co]` with one abstract method
    `__mul__` of the form `(_T_contra) -> _T_co`.

    """

    __slots__ = ()

    @abc.abstractmethod
    def __mul__(self, other: _T_contra, /) -> _T_co:
        pass


@runtime_checkable
class SupportsNeg(Protocol[_T_co]):
    """A protocol `[_T_co]` with one abstract method `__neg__` of the
    form `() -> _T_co`.

    """

    __slots__ = ()

    @abc.abstractmethod
    def __neg__(self) -> _T_co:
        pass


@runtime_checkable
class SupportsNext(Protocol[_T_co]):
    """A protocol `[_T_co]` with one abstract method `__next__` of the
    form `() -> _T_co`.

    """

    __slots__ = ()

    @abc.abstractmethod
    def __next__(self) -> _T_co:
        pass


@runtime_checkable
class SupportsObjClass(Protocol[_T_co]):
    """A protocol `[_T_co]` with one abstract property `__objclass__` of
    the form `() -> Type[_T_co]`.

    """

    __slots__ = ()

    @property
    @abc.abstractmethod
    def __objclass__(self) -> type[_T_co]:
        pass


@runtime_checkable
class SupportsOr(Protocol[_T_contra, _T_co]):
    """A protocol `[_T_contra, _T_co]` with one abstract method `__or__`
    of the form `(_T_contra) -> _T_co`.

    """

    __slots__ = ()

    @abc.abstractmethod
    def __or__(self, other: _T_contra, /) -> _T_co:
        pass


@runtime_checkable
class SupportsPos(Protocol[_T_co]):
    """A protocol `[_T_co]` with one abstract method `__pos__` of the
    form `() -> _T_co`.

    """

    __slots__ = ()

    @abc.abstractmethod
    def __pos__(self) -> _T_co:
        pass


@runtime_checkable
class SupportsPostInit(Protocol[_P]):
    """A protocol `[_P]` with one abstract method `__post_init__` of the
    form `(_P) -> None`

    """

    __slots__ = ()

    @abc.abstractmethod
    def __post_init__(self, *args: _P.args, **kwargs: _P.kwargs) -> None:
        pass


@runtime_checkable
class SupportsPow(Protocol[_T_contra, _T2_contra, _T_co]):
    """A protocol `[_T_contra, _T2_contra, _T_co]` with one abstract
    method `__pow__` of the form
    `(_T_contra, _T2_contra | None = None) -> _T_co`.

    """

    __slots__ = ()

    @abc.abstractmethod
    def __pow__(
        self, other: _T_contra, modulo: Union[_T2_contra, None] = None
    ) -> _T_co:
        pass


@runtime_checkable
class SupportsRAdd(Protocol[_T_contra, _T_co]):
    """A protocol `[_T_contra, _T_co]` with one abstract method
    `__radd__` of the form `(_T_contra) -> _T_co`.

    """

    __slots__ = ()

    @abc.abstractmethod
    def __radd__(self, other: _T_contra, /) -> _T_co:
        pass


@runtime_checkable
class SupportsRAnd(Protocol[_T_contra, _T_co]):
    """A protocol `[_T_contra, _T_co]` with one abstract method
    `__rand__` of the form `(_T_contra) -> _T_co`.

    """

    __slots__ = ()

    @abc.abstractmethod
    def __rand__(self, other: _T_contra, /) -> _T_co:
        pass


@runtime_checkable
class SupportsRDivMod(Protocol[_T_contra, _T_co]):
    """A protocol `[_T_contra, _T_co]` with one abstract method
    `__rdivmod__` of the form `(_T_contra) -> _T_co`.

    """

    __slots__ = ()

    @abc.abstractmethod
    def __rdivmod__(self, other: _T_contra, /) -> _T_co:
        pass


@runtime_checkable
class SupportsReleaseBuffer(Protocol):
    """A protocol with one abstract method `__release_buffer__` of the
    form `(memoryview) -> None`.

    """

    __slots__ = ()

    @abc.abstractmethod
    def __release_buffer__(self, buffer: memoryview, /) -> None:
        pass


@runtime_checkable
class SupportsReversed(Protocol[_T_co]):
    """A protocol `[_T_co]` with one abstract method `__reversed__` of
    the form `() -> Iterator[_T_co]`.

    """

    __slots__ = ()

    @abc.abstractmethod
    def __reversed__(self) -> Iterator[_T_co]:
        pass


@runtime_checkable
class SupportsRFloorDiv(Protocol[_T_contra, _T_co]):
    """A protocol `[_T_contra, _T_co]` with one abstract method
    `__rfloordiv__` of the form `(_T_contra) -> _T_co`.

    """

    __slots__ = ()

    @abc.abstractmethod
    def __rfloordiv__(self, other: _T_contra, /) -> _T_co:
        pass


@runtime_checkable
class SupportsRLShift(Protocol[_T_contra, _T_co]):
    """A protocol `[_T_contra, _T_co]` with one abstract method
    `__rlshift__` of the form `(_T_contra) -> _T_co`.

    """

    __slots__ = ()

    @abc.abstractmethod
    def __rlshift__(self, other: _T_contra, /) -> _T_co:
        pass


@runtime_checkable
class SupportsRMatMul(Protocol[_T_contra, _T_co]):
    """A protocol `[_T_contra, _T_co]` with one abstract method
    `__rmatmul__` of the form `(_T_contra) -> _T_co`.

    """

    __slots__ = ()

    @abc.abstractmethod
    def __rmatmul__(self, other: _T_contra, /) -> _T_co:
        pass


@runtime_checkable
class SupportsRMod(Protocol[_T_contra, _T_co]):
    """A protocol `[_T_contra, _T_co]` with one abstract method
    `__rmod__` of the form `(_T_contra) -> _T_co`.

    """

    __slots__ = ()

    @abc.abstractmethod
    def __rmod__(self, other: _T_contra, /) -> _T_co:
        pass


@runtime_checkable
class SupportsRMul(Protocol[_T_contra, _T_co]):
    """A protocol `[_T_contra, _T_co]` with one abstract method
    `__rmul__` of the form `(_T_contra) -> _T_co`.

    """

    __slots__ = ()

    @abc.abstractmethod
    def __rmul__(self, other: _T_contra, /) -> _T_co:
        pass


@runtime_checkable
class SupportsROr(Protocol[_T_contra, _T_co]):
    """A protocol `[_T_contra, _T_co]` with one abstract method
    `__ror__` of the form `(_T_contra) -> _T_co`.

    """

    __slots__ = ()

    @abc.abstractmethod
    def __ror__(self, other: _T_contra, /) -> _T_co:
        pass


@runtime_checkable
class SupportsRound(Protocol[_T_co, _T2_co]):
    """A protocol with one abstract method `__round__` of the form
    `() -> _T_co, (int) -> _T2_co`.

    """

    __slots__ = ()

    @abc.abstractmethod
    @overload
    def __round__(self) -> _T_co:
        pass

    @abc.abstractmethod
    @overload
    def __round__(self, ndigits: int, /) -> _T2_co:
        pass


@runtime_checkable
class SupportsRPow(Protocol[_T_contra, _T2_contra, _T_co]):
    """A protocol with one abstract method `__rpow__` of the form
    `(_T_contra, _T2_contra | None = None) -> _T_co`.

    """

    __slots__ = ()

    @abc.abstractmethod
    def __rpow__(
        self, other: _T_contra, modulo: Union[_T2_contra, None] = None
    ) -> _T_co:
        pass


@runtime_checkable
class SupportsRRShift(Protocol[_T_contra, _T_co]):
    """A protocol `[_T_contra, _T_co]` with one abstract method
    `__rrshift__` of the form `(_T_contra) -> _T_co`.

    """

    __slots__ = ()

    @abc.abstractmethod
    def __rrshift__(self, other: _T_contra, /) -> _T_co:
        pass


@runtime_checkable
class SupportsRShift(Protocol[_T_contra, _T_co]):
    """A protocol `[_T_contra, _T_co]` with one abstract method
    `__rshift__` of the form `(_T_contra) -> _T_co`.

    """

    __slots__ = ()

    @abc.abstractmethod
    def __rshift__(self, other: _T_contra, /) -> _T_co:
        pass


@runtime_checkable
class SupportsRSub(Protocol[_T_contra, _T_co]):
    """A protocol `[_T_contra, _T_co]` with one abstract method
    `__rsub__` of the form `(_T_contra) -> _T_co`.

    """

    __slots__ = ()

    @abc.abstractmethod
    def __rsub__(self, other: _T_contra, /) -> _T_co:
        pass


@runtime_checkable
class SupportsRTrueDiv(Protocol[_T_contra, _T_co]):
    """A protocol `[_T_contra, _T_co]` with one abstract method
    `__rtruediv__` of the form `(_T_contra) -> _T_co`.

    """

    __slots__ = ()

    @abc.abstractmethod
    def __rtruediv__(self, other: _T_contra, /) -> _T_co:
        pass


@runtime_checkable
class SupportsRXor(Protocol[_T_contra, _T_co]):
    """A protocol `[_T_contra, _T_co]` with one abstract method
    `__rxor__` of the form `(_T_contra) -> _T_co`.

    """

    __slots__ = ()

    @abc.abstractmethod
    def __rxor__(self, other: _T_contra, /) -> _T_co:
        pass


@runtime_checkable
class SupportsSet(Protocol[_T_contra, _T2_contra]):
    """A protocol with one abstract method `__set__` of the form
    `(_T_contra, _T2_contra) -> None`.

    """

    __slots__ = ()

    @abc.abstractmethod
    def __set__(self, instance: _T_contra, value: _T2_contra) -> None:
        pass


@runtime_checkable
class SupportsSetItem(Protocol[_T_contra, _T2_contra]):
    """A protocol with one abstract method `__setitem__` of the form
    `(_T_contra, _T2_contra) -> None`.

    """

    __slots__ = ()

    @abc.abstractmethod
    def __setitem__(self, key: _T_contra, value: _T2_contra, /) -> None:
        pass


@runtime_checkable
class SupportsSetName(Protocol[_T_contra]):
    """A protocol `[_T_contra]` with one abstract method `__set_name__`
    of the form `(Type[_T_contra], str) -> None`.

    """

    __slots__ = ()

    @abc.abstractmethod
    def __set_name__(self, owner: type[_T_contra], name: str, /) -> None:
        pass


@runtime_checkable
class SupportsSub(Protocol[_T_contra, _T_co]):
    """A protocol `[_T_contra, _T_co]` with one abstract method
    `__sub__` of the form `(_T_contra) -> _T_co`.

    """

    __slots__ = ()

    @abc.abstractmethod
    def __sub__(self, other: _T_contra, /) -> _T_co:
        pass


@runtime_checkable
class SupportsTrueDiv(Protocol[_T_contra, _T_co]):
    """A protocol `[_T_contra, _T_co]` with one abstract method
    `__truediv__` of the form `(_T_contra) -> _T_co`.

    """

    __slots__ = ()

    @abc.abstractmethod
    def __truediv__(self, other: _T_contra, /) -> _T_co:
        pass


@runtime_checkable
class SupportsTrunc(Protocol):
    """A protocol with one abstract method `__trunc__` of the form
    `() -> Integral`.

    """

    __slots__ = ()

    @abc.abstractmethod
    def __trunc__(self) -> int:
        pass


@runtime_checkable
class SupportsXor(Protocol[_T_contra, _T_co]):
    """A protocol `[_T_contra, _T_co]` with one abstract method
    `__xor__` of the form `(_T_contra) -> _T_co`.

    """

    __slots__ = ()

    @abc.abstractmethod
    def __xor__(self, other: _T_contra, /) -> _T_co:
        pass
