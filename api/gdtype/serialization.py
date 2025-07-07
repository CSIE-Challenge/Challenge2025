from typing import Any
from enum import IntEnum

from .defs import *

# Byte 0: `Variant::Type`, byte 1: unused, bytes 2 and 3: additional data.
HEADER_TYPE_MASK = 0xFF
# For `Variant::INT`, `Variant::FLOAT` and other math types.
HEADER_DATA_FLAG_64 = (1 << 16)
# For `Variant::ARRAY`.
HEADER_DATA_FIELD_TYPED_ARRAY_MASK = (0b11 << 16)
HEADER_DATA_FIELD_TYPED_ARRAY_SHIFT = 16


class ContainerTypeKind(IntEnum):
    NONE = 0b00
    BUILTIN = 0b01
    CLASS_NAME = 0b10
    SCRIPT = 0b11


def var_to_bytes(obj: Any) -> bytes:
    serialized = bytearray()

    def pushInt32(x: int) -> None:
        nonlocal serialized
        x = x if x >= 0 else (x + 2 ** 31)
        for _ in range(4):
            serialized.append(x & 255)
            x //= 255

    if obj is None:
        pushInt32(0)
    elif isinstance(obj, bool):
        pushInt32(TypeCode.BOOL_TYPE)
        pushInt32(int(obj))
    elif isinstance(obj, int):
        # setting ENCODE_FLAG_64 (adding 2 ** 16) sends obj as int64
        # todo: send obj as int32 instead of int64 whenever possible
        pushInt32(TypeCode.INT_TYPE + 2 ** 16)
        obj = obj if obj >= 0 else (obj + 2 ** 63)
        pushInt32(obj % (2 ** 32))
        pushInt32(obj // (2 ** 32))
    elif isinstance(obj, list):
        pushInt32(TypeCode.LIST_TYPE)
        pushInt32(len(obj))
        for i in obj:
            serialized += var_to_bytes(i)
    else:
        raise ValueError(f"[GdType] Unable to serialize variables of type '{type(obj)}'")
    
    return bytes(serialized)


def bytes_to_var(serialized: bytes) -> Any:
    if len(serialized) % 4 != 0 or len(serialized) < 4:
        raise ValueError(f"[GdType] Unable to deserialize: sequence length {len(serialized)} is not multiple of 4")
    idx = 0

    def popInt32() -> int:
        nonlocal idx
        if len(serialized) - idx < 4:
            raise ValueError(f"[GdType] Unable to deserialize: not enough data in sequence")
        result = 0
        for i in range(4):
            result = result * 256 + serialized[idx + 3 - i]
        idx += 4
        return result

    def _bytes_to_var() -> Any:
        nonlocal serialized, idx
        header = popInt32()
        typecode = header & HEADER_TYPE_MASK
        
        match typecode:
            case TypeCode.NULL_TYPE:
                return None
            
            case TypeCode.BOOL_TYPE:
                return popInt32() == 1
            
            case TypeCode.INT_TYPE:
                lo = popInt32()
                if header & HEADER_DATA_FLAG_64 != 0:
                    hi = popInt32()
                    lo = hi * (2 ** 32) + lo
                    lo = lo if lo < (2 ** 63) else (lo - 2 ** 63)
                else:
                    lo = lo if lo < (2 ** 31) else (lo - 2 ** 31)
                return lo

            case TypeCode.LIST_TYPE:
                type_kind = (header & HEADER_DATA_FIELD_TYPED_ARRAY_MASK) >> HEADER_DATA_FIELD_TYPED_ARRAY_SHIFT
                match type_kind:
                    case ContainerTypeKind.NONE:
                        pass
                    case ContainerTypeKind.BUILTIN:
                        popInt32()  # the contained type of typed arrays, but we don't need this in python
                    case _:
                        raise ValueError(f"[GdType] Unable to deserialize: unsupported array type {type_kind} at {idx - 4}")
                length = popInt32()
                result = [_bytes_to_var() for _ in range(length)]
                return result
            
            case _:
                raise ValueError(f"[GdType] Unable to deserialize: unknown type code {typecode} at {idx - 4}")
    
    return _bytes_to_var()

