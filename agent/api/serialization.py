from typing import Any
from enum import IntEnum
import struct

from .structures import Vector2


class TypeCode(IntEnum):
    NULL_TYPE = 0
    BOOL_TYPE = 1
    INT_TYPE = 2
    FLOAT_TYPE = 3
    STRING_TYPE = 4
    VECTOR2I_TYPE = 6
    DICTIONARY_TYPE = 27
    LIST_TYPE = 28


# Byte 0: `Variant::Type`, byte 1: unused, bytes 2 and 3: additional data.
HEADER_TYPE_MASK = 0xFF
# For `Variant::INT`, `Variant::FLOAT` and other math types.
HEADER_DATA_FLAG_64 = 1 << 16
# For `Variant::ARRAY`.
HEADER_DATA_FIELD_TYPED_ARRAY_MASK = 0b11 << 16
HEADER_DATA_FIELD_TYPED_ARRAY_SHIFT = 16
# For `Variant::DICTIONARY`.
# Occupies bits 16 and 17.
HEADER_DATA_FIELD_TYPED_DICTIONARY_KEY_MASK = 0b11 << 16
HEADER_DATA_FIELD_TYPED_DICTIONARY_KEY_SHIFT = 16
# Occupies bits 18 and 19.
HEADER_DATA_FIELD_TYPED_DICTIONARY_VALUE_MASK = 0b11 << 18
HEADER_DATA_FIELD_TYPED_DICTIONARY_VALUE_SHIFT = 18


class ContainerTypeKind(IntEnum):
    NONE = 0b00
    BUILTIN = 0b01
    CLASS_NAME = 0b10
    SCRIPT = 0b11


def var_to_bytes(obj: Any) -> bytes:
    serialized = bytearray()

    def pushInt32(x: int) -> None:
        nonlocal serialized
        x = x if x >= 0 else (x + 2**31)
        for _ in range(4):
            serialized.append(x & 255)
            x //= 256

    def pushFloat32(x: float) -> None:
        nonlocal serialized
        packed_bytes = struct.pack(">f", x)
        ieee_integer = struct.unpack(">I", packed_bytes)[0]
        pushInt32(ieee_integer)

    def pushFloat64(x: float) -> None:
        nonlocal serialized
        packed_bytes = struct.pack(">d", x)
        ieee_integer = struct.unpack(">Q", packed_bytes)[0]
        pushInt32(ieee_integer % (2**32))
        pushInt32(ieee_integer // (2**32))

    def pushString(value: str) -> None:
        nonlocal serialized
        encoded = bytearray(value.encode("utf-8"))
        length = len(encoded)
        while length % 4 != 0:
            encoded.append(0)
            length += 1
        pushInt32(length)
        serialized += encoded

    if obj is None:
        pushInt32(0)

    elif isinstance(obj, bool):
        pushInt32(TypeCode.BOOL_TYPE)
        pushInt32(int(obj))

    elif isinstance(obj, int):
        if -(2**31) <= obj < 2**31:
            pushInt32(TypeCode.INT_TYPE)
            obj = obj if obj >= 0 else (obj + 2**31)
            pushInt32(obj)
        else:
            pushInt32(TypeCode.INT_TYPE + HEADER_DATA_FLAG_64)
            obj = obj if obj >= 0 else (obj + 2**63)
            pushInt32(obj % (2**32))
            pushInt32(obj // (2**32))

    elif isinstance(obj, float):
        try:
            packed_bytes = struct.pack(">f", obj)
            obj_as_f32 = struct.unpack(">f", packed_bytes)[0]
            if obj_as_f32 == obj:
                pushInt32(TypeCode.FLOAT_TYPE)
                pushFloat32(obj)
            else:
                raise Exception("Value cannot be represented as float32")
        except Exception:
            pushInt32(TypeCode.FLOAT_TYPE + HEADER_DATA_FLAG_64)
            pushFloat64(obj)

    elif isinstance(obj, str):
        pushInt32(TypeCode.STRING_TYPE)
        pushString(obj)

    elif isinstance(obj, Vector2):
        pushInt32(TypeCode.VECTOR2I_TYPE)
        pushInt32(obj.x)
        pushInt32(obj.y)

    elif isinstance(obj, list):
        pushInt32(TypeCode.LIST_TYPE)
        pushInt32(len(obj))
        for i in obj:
            serialized += var_to_bytes(i)

    else:
        raise ValueError(
            f"[GdType] Unable to serialize variables of type '{type(obj)}'"
        )

    return bytes(serialized)


def bytes_to_var(serialized: bytes) -> Any:
    if len(serialized) % 4 != 0 or len(serialized) < 4:
        raise ValueError(
            f"[GdType] Unable to deserialize: sequence length {len(serialized)} is not multiple of 4"
        )
    idx = 0

    def popInt32() -> int:
        nonlocal idx
        if len(serialized) - idx < 4:
            raise ValueError(
                "[GdType] Unable to deserialize: insufficient data in sequence"
            )
        result = 0
        for i in range(4):
            result = result * 256 + serialized[idx + 3 - i]
        idx += 4
        return result

    def popFloat32() -> float:
        nonlocal idx
        if len(serialized) - idx < 4:
            raise ValueError(
                "[GdType] Unable to deserialize: insufficient data in sequence"
            )
        ieee_integer = popInt32()
        return struct.unpack(">f", struct.pack(">I", ieee_integer))[0]

    def popFloat64() -> float:
        nonlocal idx
        if len(serialized) - idx < 8:
            raise ValueError(
                "[GdType] Unable to deserialize: insufficient data in sequence"
            )
        ieee_integer = 0
        for i in range(8):
            ieee_integer = ieee_integer * 256 + serialized[idx + 7 - i]
        idx += 8
        return struct.unpack(">d", struct.pack(">Q", ieee_integer))[0]

    def popString() -> str:
        nonlocal idx
        length = popInt32()
        if len(serialized) - idx < length:
            raise ValueError(
                "[GdType] Unable to deserialize: insufficient data in sequence"
            )
        value = serialized[idx : idx + length].decode("utf-8")
        if length % 4 != 0:
            length += 4 - length % 4
        idx += length
        return value

    # the contained type of typed arrays/dictionaries, but we don't need this in python
    def popContainerType(type_kind: ContainerTypeKind) -> None:
        match type_kind:
            case ContainerTypeKind.NONE:
                pass
            case ContainerTypeKind.BUILTIN:
                popInt32()
            case _:
                raise ValueError(
                    f"[GdType] Unable to deserialize: unsupported container type {type_kind} at {idx - 4}"
                )

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
                    lo = hi * (2**32) + lo
                    lo = lo if lo < (2**63) else (lo - 2**63)
                else:
                    lo = lo if lo < (2**31) else (lo - 2**31)
                return lo

            case TypeCode.FLOAT_TYPE:
                if header & HEADER_DATA_FLAG_64 != 0:
                    return popFloat64()
                else:
                    return popFloat32()

            case TypeCode.STRING_TYPE:
                return popString()

            case TypeCode.VECTOR2I_TYPE:
                x = popInt32()
                y = popInt32()
                return Vector2(x, y)

            case TypeCode.DICTIONARY_TYPE:
                key_type_kind = ContainerTypeKind(
                    (header & HEADER_DATA_FIELD_TYPED_DICTIONARY_KEY_MASK)
                    >> HEADER_DATA_FIELD_TYPED_DICTIONARY_KEY_SHIFT
                )
                value_type_kind = ContainerTypeKind(
                    (header & HEADER_DATA_FIELD_TYPED_DICTIONARY_VALUE_MASK)
                    >> HEADER_DATA_FIELD_TYPED_DICTIONARY_VALUE_SHIFT
                )
                popContainerType(key_type_kind)
                popContainerType(value_type_kind)
                count = popInt32() & 0x7FFFFFFF
                result = {}
                for _ in range(count):
                    key = _bytes_to_var()
                    value = _bytes_to_var()
                    result[key] = value
                return result

            case TypeCode.LIST_TYPE:
                type_kind = ContainerTypeKind(
                    (header & HEADER_DATA_FIELD_TYPED_ARRAY_MASK)
                    >> HEADER_DATA_FIELD_TYPED_ARRAY_SHIFT
                )
                popContainerType(type_kind)
                length = popInt32() & 0x7FFFFFFF
                result = [_bytes_to_var() for _ in range(length)]
                return result

            case _:
                raise ValueError(
                    f"[GdType] Unable to deserialize: unsupported type code {typecode} at {idx - 4}"
                )

    return _bytes_to_var()
