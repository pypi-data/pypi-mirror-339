# Install

`$ pip install supportsx`

# Description

A Python library that supplies runtime-checkable, fully parameterized, and well-documented protocols for nearly all dunder methods/attributes.

The goal of this library is to expand what is already available in the `typing` standard library and `_typeshed` library, as well as add a number of common union protocols. The full list of available protocols can be found in [the documentation section](#documentation).

# Example

```py
from typing import Any
import supportsx

def foo(
    value: supportsx.add[Any, int],
    ctm: supportsx.u.ctx_mngr
) -> None:
    with ctm:
        print(value + 1)
```
```py
from typing import Any
from supportsx import *

def foo(
    value: SupportsAdd[Any, int],
    ctm: SupportsContextManager
) -> None:
    with ctm:
        print(value + 1)
```
As shown above, there are two ways of referencing each protocol. The preferred method is the one shown first (i.e. `supportsx.*` for primary protocols and `supportsx.u.*` for union protocols), as it helps keep the global namespace clear (although at the end of the day, it is up to you).

# Documentation

## Available Protocols

Below is an exhaustive list all available protocols, which methods/attributes they represent, and the available parameters:

### Primary protocols

| Protocol                                                      | Method/Attribute     | Parameter Order                  | Parameter Form                                                                                   |
|:--------------------------------------------------------------|:---------------------|:---------------------------------|:-------------------------------------------------------------------------------------------------|
| `supportsx.abs`<br>`supportsx.SupportsAbs`                      | `__abs__`            | `[_T_co]`                        | `() -> _T_co`                                                                                    |
| `supportsx.add`<br>`supportsx.SupportsAdd`                      | `__add__`            | `[_T_contra, _T_co]`             | `(_T_contra) -> _T_co`                                                                           |
| `supportsx.aenter`<br>`supportsx.SupportsAEnter`                | `__aenter__`         | `[_T_co]`                        | `() -> Awaitable[_T_co]`                                                                         |
| `supportsx.aexit`<br>`supportsx.SupportsAExit`                  | `__aexit__`          |                                  | `(Type[BaseException] \| None, BaseException \| None, TracebackType \| None) -> Awaitable[None]` |
| `supportsx.aiter`<br>`supportsx.SupportsAIter`                  | `__aiter__`          | `[_T_co]`                        | `() -> AsyncIterator[_T_co]`                                                                     |
| `supportsx.and_`<br>`supportsx.SupportsAnd`                     | `__and__`            | `[_T_contra, _T_co]`             | `(_T_contra) -> _T_co`                                                                           |
| `supportsx.anext`<br>`supportsx.SupportsANext`                  | `__anext__`          | `[_T_co]`                        | `() -> Awaitable[_T_co]`                                                                         |
| `supportsx.await_`<br>`supportsx.SupportsAwait`                 | `__await__`          | `[_T_co]`                        | `() -> Iterator[_T_co]`                                                                          |
| `supportsx.bool`<br>`supportsx.SupportsBool`                    | `__bool__`           |                                  | `() -> bool`                                                                                     |
| `supportsx.buffer`<br>`supportsx.SupportsBuffer`                | `__buffer__`         |                                  | `(int) -> memoryview`                                                                            |
| `supportsx.bytes`<br>`supportsx.SupportsBytes`                  | `__bytes__`          |                                  | `() -> bytes`                                                                                    |
| `supportsx.call`<br>`supportsx.SupportsCall`                    | `__call__`           | `[_P, _T_co]`                    | `(_P) -> _T_co`                                                                                  |
| `supportsx.ceil`<br>`supportsx.SupportsCeil`                    | `__ceil__`           |                                  | `() -> Integral`                                                                                 |
| `supportsx.complex`<br>`supportsx.SupportsComplex`              | `__complex__`        |                                  | `() -> complex`                                                                                  |
| `supportsx.contains`<br>`supportsx.SupportsContains`            | `__contains__`       | `[_T_contra]`                    | `(_T_contra) -> bool`                                                                            |
| `supportsx.delete`<br>`supportsx.SupportsDelete`                | `__delete__`         | `[_T_contra]`                    | `(_T_contra) -> None`                                                                            |
| `supportsx.delitem`<br>`supportsx.SupportsDelItem`              | `__delitem__`        | `[_T_contra]`                    | `(_T_contra) -> None`                                                                            |
| `supportsx.divmod`<br>`supportsx.SupportsDivMod`                | `__divmod__`         | `[_T_contra, _T_co]`             | `(_T_contra) -> _T_co`                                                                           |
| `supportsx.enter`<br>`supportsx.SupportsEnter`                  | `__enter__`          | `[_T_co]`                        | `() -> _T_co`                                                                                    |
| `supportsx.exit`<br>`supportsx.SupportsExit`                    | `__exit__`           |                                  | `(Type[BaseException] \| None, BaseException \| None, TracebackType \| None) -> None`            |
| `supportsx.float`<br>`supportsx.SupportsFloat`                  | `__float__`          |                                  | `() -> float`                                                                                    |
| `supportsx.floor`<br>`supportsx.SupportsFloor`                  | `__floor__`          |                                  | `() -> Integral`                                                                                 |
| `supportsx.floordiv`<br>`supportsx.SupportsFloorDiv`            | `__floordiv__`       | `[_T_contra, _T_co]`             | `(_T_contra) -> _T_co`                                                                           |
| `supportsx.ge`<br>`supportsx.SupportsGE`                        | `__ge__`             | `[_T_contra]`                    | `(_T_contra) -> bool`                                                                            |
| `supportsx.get`<br>`supportsx.SupportsGet`                      | `__get__`            | `[_T_contra, _T_co]`             | `(_T_contra \| None, Type[_T_contra] \| None = None) -> _T_co`                                   |
| `supportsx.getattr`<br>`supportsx.SupportsGetAttr`              | `__getattr__`        | `[_T_co]`                        | `(str) -> _T_co`                                                                                 |
| `supportsx.getitem`<br>`supportsx.SupportsGetItem`              | `__getitem__`        | `[_T_contra, _T_co]`             | `(_T_contra) -> _T_co`                                                                           |
| `supportsx.gt`<br>`supportsx.SupportsGT`                        | `__gt__`             | `[_T_contra]`                    | `(_T_contra) -> bool`                                                                            |
| `supportsx.iadd`<br>`supportsx.SupportsIAdd`                    | `__iadd__`           | `[_T_contra]`                    | `(_T_contra) -> None`                                                                            |
| `supportsx.iand`<br>`supportsx.SupportsIAnd`                    | `__iand__`           | `[_T_contra]`                    | `(_T_contra) -> None`                                                                            |
| `supportsx.ifloordiv`<br>`supportsx.SupportsIFloorDiv`          | `__ifloordiv__`      | `[_T_contra]`                    | `(_T_contra) -> None`                                                                            |
| `supportsx.ilshift`<br>`supportsx.SupportsILShift`              | `__ilshift__`        | `[_T_contra]`                    | `(_T_contra) -> None`                                                                            |
| `supportsx.imatmul`<br>`supportsx.SupportsIMatMul`              | `__imatmul__`        | `[_T_contra]`                    | `(_T_contra) -> None`                                                                            |
| `supportsx.imod`<br>`supportsx.SupportsIMod`                    | `__imod__`           | `[_T_contra]`                    | `(_T_contra) -> None`                                                                            |
| `supportsx.imul`<br>`supportsx.SupportsIMul`                    | `__imul__`           | `[_T_contra]`                    | `(_T_contra) -> None`                                                                            |
| `supportsx.index`<br>`supportsx.SupportsIndex`                  | `__index__`          |                                  | `() -> int`                                                                                      |
| `supportsx.int`<br>`supportsx.SupportsInt`                      | `__int__`            |                                  | `() -> int`                                                                                      |
| `supportsx.invert`<br>`supportsx.SupportsInvert`                | `__invert__`         | `[_T_co]`                        | `() -> _T_co`                                                                                    |
| `supportsx.ior`<br>`supportsx.SupportsIOr`                      | `__ior__`            | `[_T_contra]`                    | `(_T_contra) -> None`                                                                            |
| `supportsx.ipow`<br>`supportsx.SupportsIPow`                    | `__ipow__`           | `[_T_contra, _T2_contra]`        | `(_T_contra, _T2_contra \| None = None) -> None`                                                 |
| `supportsx.irshift`<br>`supportsx.SupportsIRShift`              | `__irshift__`        | `[_T_contra]`                    | `(_T_contra) -> None`                                                                            |
| `supportsx.isub`<br>`supportsx.SupportsISub`                    | `__isub__`           | `[_T_contra]`                    | `(_T_contra) -> None`                                                                            |
| `supportsx.iter`<br>`supportsx.SupportsIter`                    | `__iter__`           | `[_T_co]`                        | `() -> Iterator[_T_co]`                                                                          |
| `supportsx.itruediv`<br>`supportsx.SupportsITrueDiv`            | `__itruediv__`       | `[_T_contra]`                    | `(_T_contra) -> None`                                                                            |
| `supportsx.ixor`<br>`supportsx.SupportsIXor`                    | `__ixor__`           | `[_T_contra]`                    | `(_T_contra) -> None`                                                                            |
| `supportsx.le`<br>`supportsx.SupportsLE`                        | `__le__`             | `[_T_contra]`                    | `(_T_contra) -> bool`                                                                            |
| `supportsx.len`<br>`supportsx.SupportsLen`                      | `__len__`            |                                  | `() -> int`                                                                                      |
| `supportsx.length_hint`<br>`supportsx.SupportsLengthHint`       | `__length_hint__`    |                                  | `() -> int`                                                                                      |
| `supportsx.lshift`<br>`supportsx.SupportsLShift`                | `__lshift__`         | `[_T_contra, _T_co]`             | `(_T_contra) -> _T_co`                                                                           |
| `supportsx.lt`<br>`supportsx.SupportsLT`                        | `__lt__`             | `[_T_contra]`                    | `(_T_contra) -> bool`                                                                            |
| `supportsx.match_args`<br>`supportsx.SupportsMatchArgs`         | `__match_args__`     |                                  | `() -> Sequence[str]`                                                                            |
| `supportsx.matmul`<br>`supportsx.SupportsMatMul`                | `__matmul__`         | `[_T_contra, _T_co]`             | `(_T_contra) -> _T_co`                                                                           |
| `supportsx.missing`<br>`supportsx.SupportsMissing`              | `__missing__`        | `[_T_contra, _T_co]`             | `(_T_contra) -> _T_co`                                                                           |
| `supportsx.mod`<br>`supportsx.SupportsMod`                      | `__mod__`            | `[_T_contra, _T_co]`             | `(_T_contra) -> _T_co`                                                                           |
| `supportsx.mro_entries`<br>`supportsx.SupportsMroEntries`       | `__mro_entries__`    | `[_T]`                           | `(Sequence[_T]) -> Sequence[_T]`                                                                 |
| `supportsx.mul`<br>`supportsx.SupportsMul`                      | `__mul__`            | `[_T_contra, _T_co]`             | `(_T_contra) -> _T_co`                                                                           |
| `supportsx.neg`<br>`supportsx.SupportsNeg`                      | `__neg__`            | `[_T_co]`                        | `() -> _T_co`                                                                                    |
| `supportsx.next`<br>`supportsx.SupportsNext`                    | `__next__`           | `[_T_co]`                        | `() -> _T_co`                                                                                    |
| `supportsx.objclass`<br>`supportsx.SupportsObjClass`            | `__objclass__`       | `[_T_co]`                        | `() -> Type[_T_co]`                                                                              |
| `supportsx.or_`<br>`supportsx.SupportsOr`                       | `__or__`             | `[_T_contra, _T_co]`             | `(_T_contra) -> _T_co`                                                                           |
| `supportsx.pos`<br>`supportsx.SupportsPos`                      | `__pos__`            | `[_T_co]`                        | `() -> _T_co`                                                                                    |
| `supportsx.post_init`<br>`supportsx.SupportsPostInit`           | `__post_init__`      | `[_P]`                           | `(_P) -> None`                                                                                   |
| `supportsx.pow`<br>`supportsx.SupportsPow`                      | `__pow__`            | `[_T_contra, _T2_contra, _T_co]` | `(_T_contra, _T2_contra \| None = None) -> _T_co`                                                |
| `supportsx.radd`<br>`supportsx.SupportsRAdd`                    | `__radd__`           | `[_T_contra, _T_co]`             | `(_T_contra) -> _T_co`                                                                           |
| `supportsx.rand`<br>`supportsx.SupportsRAnd`                    | `__rand__`           | `[_T_contra, _T_co]`             | `(_T_contra) -> _T_co`                                                                           |
| `supportsx.rdivmod`<br>`supportsx.SupportsRDivMod`              | `__rdivmod__`        | `[_T_contra, _T_co]`             | `(_T_contra) -> _T_co`                                                                           |
| `supportsx.release_buffer`<br>`supportsx.SupportsReleaseBuffer` | `__release_buffer__` |                                  | `(memoryview) -> None`                                                                           |
| `supportsx.reversed`<br>`supportsx.SupportsReversed`            | `__reversed__`       | `[_T_co]`                        | `() -> Iterator[_T_co]`                                                                          |
| `supportsx.rfloordiv`<br>`supportsx.SupportsRFloorDiv`          | `__rfloordiv__`      | `[_T_contra, _T_co]`             | `(_T_contra) -> _T_co`                                                                           |
| `supportsx.rlshift`<br>`supportsx.SupportsRLShift`              | `__rlshift__`        | `[_T_contra, _T_co]`             | `(_T_contra) -> _T_co`                                                                           |
| `supportsx.rmatmul`<br>`supportsx.SupportsRMatMul`              | `__rmatmul__`        | `[_T_contra, _T_co]`             | `(_T_contra) -> _T_co`                                                                           |
| `supportsx.rmod`<br>`supportsx.SupportsRMod`                    | `__rmod__`           | `[_T_contra, _T_co]`             | `(_T_contra) -> _T_co`                                                                           |
| `supportsx.rmul`<br>`supportsx.SupportsRMul`                    | `__rmul__`           | `[_T_contra, _T_co]`             | `(_T_contra) -> _T_co`                                                                           |
| `supportsx.ror`<br>`supportsx.SupportsROr`                      | `__ror__`            | `[_T_contra, _T_co]`             | `(_T_contra) -> _T_co`                                                                           |
| `supportsx.round`<br>`supportsx.SupportsRound`                  | `__round__`          | `[_T_co, _T2_co]`                | `() -> _T_co, (int) -> _T2_co`                                                                   |
| `supportsx.rpow`<br>`supportsx.SupportsRPow`                    | `__rpow__`           | `[_T_contra, _T2_contra, _T_co]` | `(_T_contra, _T2_contra \| None = None) -> _T_co`                                                |
| `supportsx.rrshift`<br>`supportsx.SupportsRRShift`              | `__rrshift__`        | `[_T_contra, _T_co]`             | `(_T_contra) -> _T_co`                                                                           |
| `supportsx.rshift`<br>`supportsx.SupportsRShift`                | `__rshift__`         | `[_T_contra, _T_co]`             | `(_T_contra) -> _T_co`                                                                           |
| `supportsx.rsub`<br>`supportsx.SupportsRSub`                    | `__rsub__`           | `[_T_contra, _T_co]`             | `(_T_contra) -> _T_co`                                                                           |
| `supportsx.rtruediv`<br>`supportsx.SupportsRTrueDiv`            | `__rtruediv__`       | `[_T_contra, _T_co]`             | `(_T_contra) -> _T_co`                                                                           |
| `supportsx.rxor`<br>`supportsx.SupportsRXor`                    | `__rxor__`           | `[_T_contra, _T_co]`             | `(_T_contra) -> _T_co`                                                                           |
| `supportsx.set`<br>`supportsx.SupportsSet`                      | `__set__`            | `[_T_contra, _T2_contra]`        | `(_T_contra, _T2_contra) -> None`                                                                |
| `supportsx.setitem`<br>`supportsx.SupportsSetItem`              | `__setitem__`        | `[_T_contra, _T2_contra]`        | `(_T_contra, _T2_contra) -> None`                                                                |
| `supportsx.set_name`<br>`supportsx.SupportsSetName`             | `__set_name__`       | `[_T_contra]`                    | `(Type[_T_contra], str) -> None`                                                                 |
| `supportsx.sub`<br>`supportsx.SupportsSub`                      | `__sub__`            | `[_T_contra, _T_co]`             | `(_T_contra) -> _T_co`                                                                           |
| `supportsx.truediv`<br>`supportsx.SupportsTrueDiv`              | `__truediv__`        | `[_T_contra, _T_co]`             | `(_T_contra) -> _T_co`                                                                           |
| `supportsx.trunc`<br>`supportsx.SupportsTrunc`                  | `__trunc__`          |                                  | `() -> Integral`                                                                                 |
| `supportsx.xor`<br>`supportsx.SupportsXor`                      | `__xor__`            | `[_T_contra, _T_co]`             | `(_T_contra) -> _T_co`                                                                           |

### Union Protocols

| Protocol                                                                                                        | Parameters (in order)                        | Bases                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
|:----------------------------------------------------------------------------------------------------------------|:---------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `supportsx.u.actx_mngr`<br>`supportsx.SupportsAsyncContextManager`<br>`supportsx.u.SupportsAsyncContextManager` | `[_T_co]`                                    | `SupportsAEnter[_T_co]`<br>`SupportsAExit`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| `supportsx.u.bitops`<br>`supportsx.SupportsBitwiseOps`<br>`supportsx.u.SupportsBitwiseOps`                      | `[_T_contra, _T_co]`                         | `SupportsAnd[_T_contra, _T_co]`<br>`SupportsLShift[_T_contra, _T_co]`<br>`SupportsOr[_T_contra, _T_co]`<br>`SupportsRAnd[_T_contra, _T_co]`<br>`SupportsRLShift[_T_contra, _T_co]`<br>`SupportsROr[_T_contra, _T_co]`<br>`SupportsRRShift[_T_contra, _T_co]`<br>`SupportsRShift[_T_contra, _T_co]`<br>`SupportsRXor[_T_contra, _T_co]`<br>`SupportsXor[_T_contra, _T_co]`                                                                                                                                                                               |
| `supportsx.u.cmps`<br>`supportsx.SupportsComparisons`<br>`supportsx.u.SupportsComparisons`                      | `[_T_contra]`                                | `SupportsGE[_T_contra]`<br>`SupportsGT[_T_contra]`<br>`SupportsLE[_T_contra]`<br>`SupportsLT[_T_contra]`                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| `supportsx.u.ctx_mngr`<br>`supportsx.SupportsContextManager`<br>`supportsx.u.SupportsContextManager`            | `[_T_co]`                                    | `SupportsEnter[_T_co]<br>SupportsExit`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| `supportsx.u.data_desc`<br>`supportsx.SupportsDataDescriptor`<br>`supportsx.u.SupportsDataDescriptor`           | `[_T_contra, _T2_contra, _T_co]`             | `SupportsDelete[_T_contra]`<br>`SupportsGet[_T_contra, _T_co]`<br>`SupportsSet[_T_contra, _T2_contra]`                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| `supportsx.u.ibitops`<br>`supportsx.SupportsIBitwiseOps`<br>`supportsx.u.SupportsIBitwiseOps`                   | `[_T_contra]`                                | `SupportsIAnd[_T_contra]`<br>`SupportsILShift[_T_contra]`<br>`SupportsIOr[_T_contra]`<br>`SupportsIRShift[_T_contra]`<br>`SupportsIXor[_T_contra]`                                                                                                                                                                                                                                                                                                                                                                                                      |
| `supportsx.u.imathops`<br>`supportsx.SupportsIMathOps`<br>`supportsx.u.SupportsIMathOps`                        | `[_T_contra, _T2_contra]`                    | `SupportsIAdd[_T_contra]`<br>`SupportsIFloorDiv[_T_contra]`<br>`SupportsIMod[_T_contra]`<br>`SupportsIMul[_T_contra]`<br>`SupportsIPow[_T_contra, _T2_contra]`<br>`SupportsISub[_T_contra]`<br>`SupportsITrueDiv[_T_contra]`                                                                                                                                                                                                                                                                                                                            |
| `supportsx.u.imathops2`<br>`supportsx.SupportsIMathOps2`<br>`supportsx.u.SupportsIMathOps2`                     | `[_T_contra, _T2_contra]`                    | `SupportsIMathOps[_T_contra, _T2_contra]`<br>`SupportsIMatMul[_T_contra]`                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| `supportsx.u.items`<br>`supportsx.SupportsItems`<br>`supportsx.u.SupportsItems`                                 | `[_T_contra, _T2_contra, _T_co]`             | `SupportsDelItem[_T_contra]`<br>`SupportsGetItem[_T_contra, _T_co]`<br>`SupportsSetItem[_T_contra, _T2_contra]`                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| `supportsx.u.length`<br>`supportsx.SupportsLength`<br>`supportsx.u.SupportsLength`                              |                                              | `SupportsLen`<br>`SupportsLengthHint`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| `supportsx.u.math_funcs`<br>`supportsx.SupportsMathFunctions`<br>`supportsx.u.SupportsMathFunctions`            | `[_T_contra, _T_co, _T2_co, _T3_co, _T4_co]` | `SupportsAbs[_T2_co]`<br>`SupportsCeil`<br>`SupportsDivMod[_T_contra, _T_co]`<br>`SupportsFloor`<br>`SupportsRDivMod[_T_contra, _T_co]`<br>`SupportsRound[_T3_co, _T4_co]`<br>`SupportsTrunc`                                                                                                                                                                                                                                                                                                                                                           |
| `supportsx.u.mathops`<br>`supportsx.SupportsMathOps`<br>`supportsx.u.SupportsMathOps`                           | `[_T_contra, _T2_contra, _T_co]`             | `SupportsAdd[_T_contra, _T_co]`<br>`SupportsFloorDiv[_T_contra, _T_co]`<br>`SupportsMod[_T_contra, _T_co]`<br>`SupportsMul[_T_contra, _T_co]`<br>`SupportsPow[_T_contra, _T2_contra, _T_co]`<br>`SupportsRAdd[_T_contra, _T_co]`<br>`SupportsRFloorDiv[_T_contra, _T_co]`<br>`SupportsRMod[_T_contra, _T_co]`<br>`SupportsRMul[_T_contra, _T_co]`<br>`SupportsRPow[_T_contra, _T2_contra, _T_co]`<br>`SupportsRSub[_T_contra, _T_co]`<br>`SupportsRTrueDiv[_T_contra, _T_co]`<br>`SupportsSub[_T_contra, _T_co]`<br>`SupportsTrueDiv[_T_contra, _T_co]` |
| `supportsx.u.mathops2`<br>`supportsx.SupportsMathOps2`<br>`supportsx.u.SupportsMathOps2`                        | `[_T_contra, _T2_contra, _T_co]`             | `SupportsMathOps[_T_contra, _T2_contra, _T_co]`<br>`SupportsMatMul[_T_contra, _T_co]`<br>`SupportsRMatMul[_T_contra, _T_co]`                                                                                                                                                                                                                                                                                                                                                                                                                            |
| `supportsx.u.type_conversion`<br>`supportsx.SupportsTypeConversion`<br>`supportsx.u.SupportsTypeConversion`     |                                              | `SupportsBytes`<br>`SupportsComplex`<br>`SupportsFloat`<br>`SupportsIndex`<br>`SupportsInt`                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| `supportsx.u.type_conversion2`<br>`supportsx.SupportsTypeConversion2`<br>`supportsx.u.SupportsTypeConversion2`  |                                              | `SupportsBool`<br>`SupportsTypeConversion`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| `supportsx.u.unary_ops`<br>`supportsx.SupportsUnaryOps`<br>`supportsx.u.SupportsUnaryOps`                       | `[_T_co]`                                    | `SupportsInvert[_T_co]`<br>`SupportsNeg[_T_co]`<br>`SupportsPos[_T_co]`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |

## Excluded Methods and Attributes

The following methods are available on all objects, and are thus excluded:

|                     |
|:--------------------|
| `__delattr__`       |
| `__dir__`           |
| `__eq__`            |
| `__format__`        |
| `__getattribute__`  |
| `__getstate__`      |
| `__hash__`          |
| `__init__`          |
| `__init_subclass__` |
| `__ne__`            |
| `__new__`           |
| `__reduce__`        |
| `__reduce_ex__`     |
| `__repr__`          |
| `__setattr__`       |
| `__sizeof__`        |
| `__str__`           |
| `__subclasshook__`  |

The following methods are available on all types, and are thus excluded:

|                     |
|:--------------------|
| `__instancecheck__` |
| `__prepare__`       |
| `__subclasscheck__` |
| `__subclasses__`    |
| `mro`               |

The following attributes are available on all types, and are thus excluded:

|                      |
|:---------------------|
| `__base__`           |
| `__bases__`          |
| `__basicsize__`      |
| `__class__`          |
| `__dictoffset__`     |
| `__flags__`          |
| `__itemsize__`       |
| `__module__`         |
| `__mro__`            |
| `__name__`           |
| `__qualname__`       |
| `__text_signature__` |
| `__type_params__`    |
| `__weakrefoffset__`  |

Although `__slots__` and `__dict__` may not appear on an object, protocols for those objects are not currently supported by the Python specification due to the part they play in attribute access.
