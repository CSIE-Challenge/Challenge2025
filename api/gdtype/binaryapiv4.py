# MIT License
#
# Copyright (c) 2022 Arkadiusz Netczuk <dev.arnet@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

import logging
from enum import IntEnum, unique

from . import commontypes as ct

from .commontypes import Vector2, Vector2i, Rect2, Rect2i,\
    Vector3, Vector3i, Transform2D, Vector4, Vector4i, Plane, Quaternion, AABB,\
    Basis, Transform3D, Projection, Color, StringName, NodePath, RID
from .commontypes import ByteArray,\
    Int32Array, Int64Array, Float32Array, Float64Array, StringArray,\
    Vector2Array, Vector3Array, ColorArray


_LOGGER = logging.getLogger(__name__)


##
## interface functions
##
deserialize        = ct.deserialize
serialize          = ct.serialize
get_message_length = ct.get_message_length
check_message_size = ct.check_message_size


## ============================================================


@unique
class GodotType( IntEnum ):
    NULL                = 0
    BOOL                = 1
    INT                 = 2
    FLOAT               = 3
    STRING              = 4
    VECTOR2             = 5
    VECTOR2I            = 6
    RECT2               = 7
    RECT2I              = 8
    VECTOR3             = 9
    VECTOR3I            = 10
    TRANSFORM2D         = 11
    VECTOR4             = 12
    VECTOR4I            = 13
    PLANE               = 14
    QUATERNION          = 15
    AABB                = 16
    BASIS               = 17
    TRANSFORM3D         = 18
    PROJECTION          = 19
    COLOR               = 20
    STRINGNAME          = 21
    NODEPATH            = 22
    RID                 = 23
#     OBJECT              = 24
#     CALLABLE            = 25
#     SIGNAL              = 26
    DICT                = 27
    LIST                = 28
    PACKEDBYTEARRAY     = 29
    PACKEDINT32ARRAY    = 30
    PACKEDINT64ARRAY    = 31
    PACKEDFLOAT32ARRAY  = 32
    PACKEDFLOAT64ARRAY  = 33
    PACKEDSTRINGARRAY   = 34
    PACKEDVECTOR2ARRAY  = 35
    PACKEDVECTOR3ARRAY  = 36
    PACKEDCOLORARRAY    = 37

    @classmethod
    def fromInt(cls, value):
        try:
            return GodotType( value )
        except ValueError as ex:
            raise ValueError( f"unsupported Godot type: {value}" ) from ex


## types configuration for serialization and deserialization
## <deserialize_function> converts given Godot type in form of binary array into Python equivalent
## <serialize_function>   converts Python value into binary array representing Godot type
## configuration accepts two formats"
##     explicit: ( Godot_Type_Id, Python_Type, <deserialize_function>, <serialize_function> )
##     implicit: ( Godot_Type_Id, Python_Type )
##                where <deserialize_function> is "deserialize_Python_Type"
##                where <serialize_function>   is "serialize_Python_Type"
CONFIG_LIST = [
    ( GodotType.NULL.value,                 type(None),       ct.deserialize_none,         ct.serialize_none ),
    ( GodotType.BOOL.value,                 bool,             ct.deserialize_bool,         ct.serialize_bool ),
    ( GodotType.INT.value,                  int,              ct.deserialize_int,          ct.serialize_int ),
    ( GodotType.FLOAT.value,                float,            ct.deserialize_float,        ct.serialize_float ),
    ( GodotType.STRING.value,               str,              ct.deserialize_string,       ct.serialize_string ),
    ( GodotType.VECTOR2.value,              Vector2 ),
    ( GodotType.VECTOR2I.value,             Vector2i ),
    ( GodotType.RECT2.value,                Rect2 ),
    ( GodotType.RECT2I.value,               Rect2i ),
    ( GodotType.VECTOR3.value,              Vector3 ),
    ( GodotType.VECTOR3I.value,             Vector3i ),
    ( GodotType.TRANSFORM2D.value,          Transform2D ),
    ( GodotType.VECTOR4.value,              Vector4 ),
    ( GodotType.VECTOR4I.value,             Vector4i ),
    ( GodotType.PLANE.value,                Plane ),
    ( GodotType.QUATERNION.value,           Quaternion ),
    ( GodotType.AABB.value,                 AABB ),
    ( GodotType.BASIS.value,                Basis ),
    ( GodotType.TRANSFORM3D.value,          Transform3D ),
    ( GodotType.PROJECTION.value,           Projection ),
    ( GodotType.COLOR.value,                Color ),
    ( GodotType.STRINGNAME.value,           StringName ),
    ( GodotType.NODEPATH.value,             NodePath ),
    ( GodotType.RID.value,                  RID ),
    ( GodotType.DICT.value,                 dict,             ct.deserialize_dict,         ct.serialize_dict ),
    ( GodotType.LIST.value,                 list,             ct.deserialize_list,         ct.serialize_list ),
    ( GodotType.PACKEDBYTEARRAY.value,      ByteArray ),
    ( GodotType.PACKEDINT32ARRAY.value,     Int32Array ),
    ( GodotType.PACKEDINT64ARRAY.value,     Int64Array ),
    ( GodotType.PACKEDFLOAT32ARRAY.value,   Float32Array ),
    ( GodotType.PACKEDFLOAT64ARRAY.value,   Float64Array ),
    ( GodotType.PACKEDSTRINGARRAY.value,    StringArray ),
    ( GodotType.PACKEDVECTOR2ARRAY.value,   Vector2Array ),
    ( GodotType.PACKEDVECTOR3ARRAY.value,   Vector3Array ),
    ( GodotType.PACKEDCOLORARRAY.value,     ColorArray )

    # ( GodotType.BOOL.value,  bool,        deserialize_uninplemented,  serialize_uninplemented ),
]


## ======================================================================


##
## DESERIALIZATION_MAP: Dict[ Godot_Type_Id, <deserialize_function> ]
## SERIALIZATION_MAP:   Dict[ Python_Type, (Godot_Type_Id, <serialize_function>) ]
##
DESERIALIZATION_MAP, SERIALIZATION_MAP = ct.prepare_config_dicts( CONFIG_LIST, ct )


def get_deserialization_function_v4( gd_type_id: int ):
    deserialize_function = DESERIALIZATION_MAP.get( gd_type_id, None )
    if deserialize_function is None:
        raise ValueError( f"invalid CONFIG_LIST: unsupported Godot type {gd_type_id}" )
    return deserialize_function


def get_serialization_config_v4( py_type: type ):
    return SERIALIZATION_MAP.get( py_type, None )


## override 'abstract' functions
ct.get_deserialization_function = get_deserialization_function_v4
ct.get_serialization_config     = get_serialization_config_v4
