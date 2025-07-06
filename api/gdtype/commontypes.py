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

# pylint: disable=invalid-name
# pylint: disable=too-many-lines

import logging
from dataclasses import dataclass, field

import numpy

from typing import List, Tuple
from typing import Dict, Callable, Any
from types import FunctionType

from .bytescontainer import BytesContainer


_LOGGER = logging.getLogger(__name__)


def deserialize( message: bytes ):
    return deserialize_custom( message, deserialize_type )

    # mess_len = len( message )
    # if mess_len < 4:
    #     _LOGGER.error( "invalid packet -- too short: %s", message )
    #     raise ValueError( f"invalid packet -- too short: {mess_len} < 4 for {message!r}" )
    #
    # data = BytesContainer( message )
    # expected_size = data.popInt32()
    # message_size  = data.size()
    # if message_size != expected_size:
    #     _LOGGER.error( "invalid packet -- packet size mismatch data size: %s", data )
    #     raise ValueError( f"message size mismatch: {message_size} != {expected_size} for {data}" )
    #
    # return deserialize_type( data )


def deserialize_custom( message: bytes, deserialize_function ):
    mess_len = len( message )
    if mess_len < 4:
        _LOGGER.error( "invalid packet -- too short: %s", message )
        raise ValueError( f"invalid packet -- too short: {mess_len} < 4 for {message!r}" )

    data = BytesContainer( message )
    expected_size = data.popInt32()
    message_size  = data.size()
    if message_size != expected_size:
        _LOGGER.error( "invalid packet -- packet size mismatch data size: %s", data )
        raise ValueError( f"message size mismatch: {message_size} != {expected_size} for {data}" )

    data_len = data.size()
    if data_len < 4:
        raise ValueError( f"invalid packet -- too short: {data}" )

    return deserialize_function( data )


def serialize( value ) -> bytes:
    return serialize_custom( value, serialize_type )

    # data = BytesContainer()
    # serialize_type( value, data )
    # data_size = data.size()
    # if data_size < 1:
    #     ## failed to serialize data
    #     raise ValueError( "failed to serialize: empty output data" )
    # message = BytesContainer()
    # message.pushInt32( data_size )        ## set header
    # message.push( data.data )
    # return message.data


def serialize_custom( value, serialize_function ) -> bytes:
    data = BytesContainer()
    serialize_function( value, data )
    data_size = data.size()
    if data_size < 1:
        ## failed to serialize data
        raise ValueError( "failed to serialize: empty output data" )
    message = BytesContainer()
    message.pushInt32( data_size )        ## set header
    message.push( data.data )
    return message.data


## read header value of message and return it
def get_message_length( data: bytes ):
    container = BytesContainer( data )
    if container.size() < 4:
        _LOGGER.error( "message is too short: %s", data )
        return None
    return container.popInt32()


## return:
##        0         if buffer contains full message without additional bytes
##        negative  if there is missing data (how many bytes are missing)
##        positive  if there are additional bytes (part of next message in case of TCP/IP)
##
## whole message consists of header and remaining data
## header is 4 bytes integer containing size of remaining data
## so whole message is sum of value in header increased by size of header itself
def check_message_size( buffer: bytes ):
    curr_size = len( buffer )
    if curr_size < 4:
        return -4 + curr_size
    expected_size = get_message_length( buffer )
    expected_size += 4                              ## increase by message header
    return curr_size - expected_size


## ======================================================================
## ======================================================================


## returns Python equivalent of given data
def deserialize_type( data: BytesContainer ):
    data_len = data.size()
    if data_len < 4:
        raise ValueError( f"invalid packet -- too short: {data}" )

    data_flags, gd_type_id = data.popFlagsType()

    deserialize_function = get_deserialization_function( gd_type_id )
    if deserialize_function is None:
        raise ValueError( f"unable to get deserialization info for Godot type {gd_type_id}" )

    return deserialize_function( data_flags, data )


## serialize into 'data' given Python 'value' as binary representation of Godot equivalent
def serialize_type( value, data: BytesContainer ):
    value_type = type( value )

    serialize_config = get_serialization_config( value_type )
#     serialize_config = SERIALIZATION_MAP.get( value_type, None )
    if serialize_config is None:
        #_LOGGER.warning( "unable to serialize data: %s %s", value, type(value) )
        raise ValueError( f"unable to serialize data: {value} {type(value)}" )

    gd_type_id         = serialize_config[0]
    serialize_function = serialize_config[1]

    serialize_function( gd_type_id, value, data )


## =========================================================


##
## Returns function of ( int, BytesContainer ) -> Any
## where Any depends on 'gd_type_id'.
## Example of returned function 'deserialize_float'.
##
def get_deserialization_function( gd_type_id: int ):
    raise NotImplementedError( "stub function: implement and import proper function" )


##
## Returns pair: ( int, ( int, Any, BytesContainer ) -> void )
## consists on pair containing Godot type ID and serialization function.
## Example of returned function 'serialize_float'.
##
def get_serialization_config( py_type: type ):
    raise NotImplementedError( "stub function: implement and import proper function" )


## =========================================================


def deserialize_uninplemented( data_flags: int, data: BytesContainer ):
    raise NotImplementedError( "stub deserialization used: implement/use proper function" )


def serialize_uninplemented( gd_type_id: int, value, data: BytesContainer ):
    raise NotImplementedError( "stub serialization used: implement/use proper function" )


## =========================================================


def deserialize_none( _: int, _2: BytesContainer ):
    return None


def serialize_none( gd_type_id: int, _, data: BytesContainer ):
    data.pushFlagsType( 0, gd_type_id )


## =========================================================


# def deserialize_bool( data_flags: int, data: BytesContainer ):
def deserialize_bool( _: int, data: BytesContainer ):
    data_len = data.size()
    if data_len < 4:
        _LOGGER.error( "invalid packet -- too short: %s", data )
        raise ValueError( f"invalid packet -- too short: {data}" )
    data_value = data.popInt32()
    proper_data = data_value > 0
    return proper_data


def serialize_bool( gd_type_id: int, value, data: BytesContainer ):
    data.pushFlagsType( 0, gd_type_id )
    data.pushInt32( value )


## =========================================================


# def deserialize_int( data_flags: int, data: BytesContainer ):
def deserialize_int( _: int, data: BytesContainer ):
    data_len = data.size()
    if data_len < 4:
        raise ValueError( f"invalid packet -- too short: {data}" )
    return data.popInt32()


def serialize_int( gd_type_id: int, value, data: BytesContainer ):
    data.pushFlagsType( 0, gd_type_id )
    data.pushInt32( value )


## =========================================================


def deserialize_float( data_flags: int, data: BytesContainer ) -> float:
    data_len = data.size()
    encoded_64 = (data_flags & 1) == 1
    if encoded_64:
        if data_len < 8:
            raise ValueError( f"invalid packet -- too short: {data}" )
        proper_data = data.popFloat64()
        return proper_data
    ## 32 bit variant
    if data_len < 4:
        raise ValueError( f"invalid packet -- too short: {data}" )
    proper_data = data.popFloat32()
    return proper_data


def serialize_float( gd_type_id: int, value: float, data: BytesContainer ):
    data.pushFlagsType( 1, gd_type_id )
    data.pushFloat64( value )


## =========================================================


# def deserialize_string( data_flags: int, data: BytesContainer ):
def deserialize_string( _: int, data: BytesContainer ) -> str:
    data_len = data.size()
    if data_len < 4:
        raise ValueError( f"invalid packet -- too short: {data}" )
    return data.popString()


def serialize_string( gd_type_id: int, value: str, data: BytesContainer ):
    data.pushFlagsType( 0, gd_type_id )
    str_len = len( value )
    data.pushInt32( str_len )
    data.pushStringRaw( value )
    remaining = str_len % 4
    if remaining > 0:
        padding = 4 - remaining
        data.pushZeros( padding )


## =========================================================


@dataclass
class Vector2():
    x: float = 0.0
    y: float = 0.0

    def __init__( self, data_array=None ):
        if data_array is None:
            return
        if len(data_array) != 2:
            raise ValueError( f"invalid array size: {data_array}" )
        self.x = data_array[0]
        self.y = data_array[1]

    def getDataArray(self):
        return [ self.x, self.y ]


def deserialize_Vector2( _: int, data: BytesContainer ) -> Vector2:
    data = data.popFloat32Items(2)
    return Vector2( data )


def serialize_Vector2( gd_type_id: int, value: Vector2, data: BytesContainer ):
    data.pushFlagsType( 0, gd_type_id )
    data_array = value.getDataArray()
    data.pushFloat32Items( data_array )


## =========================================================


@dataclass
class Vector2i():
    x: int = 0
    y: int = 0

    def __init__( self, data_array=None ):
        if data_array is None:
            return
        if len(data_array) != 2:
            raise ValueError( f"invalid array size: {data_array}" )
        self.x = data_array[0]
        self.y = data_array[1]

    def getDataArray(self):
        return [ self.x, self.y ]


def deserialize_Vector2i( _: int, data: BytesContainer ) -> Vector2i:
    data = data.popInt32Items(2)
    return Vector2i( data )


def serialize_Vector2i( gd_type_id: int, value: Vector2i, data: BytesContainer ):
    data.pushFlagsType( 0, gd_type_id )
    data_array = value.getDataArray()
    data.pushInt32Items( data_array )


## =========================================================


@dataclass
class Rect2():
    x_coord: float = 0.0
    y_coord: float = 0.0
    x_size: float  = 0.0
    y_size: float  = 0.0

    def __init__( self, data_array=None ):
        if data_array is None:
            return
        if len(data_array) != 4:
            raise ValueError( f"invalid array size: {data_array}" )
        self.x_coord = data_array[0]
        self.y_coord = data_array[1]
        self.x_size  = data_array[2]
        self.y_size  = data_array[3]

    def getDataArray(self):
        return [ self.x_coord, self.y_coord, self.x_size, self.y_size ]


def deserialize_Rect2( _: int, data: BytesContainer ) -> Rect2:
    data = data.popFloat32Items(4)
    return Rect2( data )


def serialize_Rect2( gd_type_id: int, value: Rect2, data: BytesContainer ):
    data.pushFlagsType( 0, gd_type_id )
    data_array = value.getDataArray()
    data.pushFloat32Items( data_array )


## =========================================================


@dataclass
class Rect2i():
    x_coord: int = 0
    y_coord: int = 0
    x_size: int  = 0
    y_size: int  = 0

    def __init__( self, data_array=None ):
        if data_array is None:
            return
        if len(data_array) != 4:
            raise ValueError( f"invalid array size: {data_array}" )
        self.x_coord = data_array[0]
        self.y_coord = data_array[1]
        self.x_size  = data_array[2]
        self.y_size  = data_array[3]

    def getDataArray(self):
        return [ self.x_coord, self.y_coord, self.x_size, self.y_size ]


def deserialize_Rect2i( _: int, data: BytesContainer ) -> Rect2i:
    data = data.popInt32Items(4)
    return Rect2i( data )


def serialize_Rect2i( gd_type_id: int, value: Rect2i, data: BytesContainer ):
    data.pushFlagsType( 0, gd_type_id )
    data_array = value.getDataArray()
    data.pushInt32Items( data_array )


## =========================================================


@dataclass
class Vector3():
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0

    def __init__( self, data_array=None ):
        if data_array is None:
            return
        if len(data_array) != 3:
            raise ValueError( f"invalid array size: {data_array}" )
        self.x = data_array[0]
        self.y = data_array[1]
        self.z = data_array[2]

    def getDataArray(self):
        return [ self.x, self.y, self.z ]


# def deserialize_vector3( data_flags: int, data: BytesContainer ):
def deserialize_Vector3( _: int, data: BytesContainer ) -> Vector3:
    data = data.popFloat32Items(3)
    return Vector3( data )


def serialize_Vector3( gd_type_id: int, value: Vector3, data: BytesContainer ):
    data.pushFlagsType( 0, gd_type_id )
    data_array = value.getDataArray()
    data.pushFloat32Items( data_array )


## =========================================================


@dataclass
class Vector3i():
    x: int = 0
    y: int = 0
    z: int = 0

    def __init__( self, data_array=None ):
        if data_array is None:
            return
        if len(data_array) != 3:
            raise ValueError( f"invalid array size: {data_array}" )
        self.x = data_array[0]
        self.y = data_array[1]
        self.z = data_array[2]

    def getDataArray(self):
        return [ self.x, self.y, self.z ]


def deserialize_Vector3i( _: int, data: BytesContainer ) -> Vector3i:
    data = data.popInt32Items(3)
    return Vector3i( data )


def serialize_Vector3i( gd_type_id: int, value: Vector3i, data: BytesContainer ):
    data.pushFlagsType( 0, gd_type_id )
    data_array = value.getDataArray()
    data.pushInt32Items( data_array )


## =========================================================


@dataclass
class Transform2D():
    ## has 2 rows and 3 columns
    values: list

    def __init__( self, data_array=None ):
        if data_array is None:
            self.values: list = [ 0.0 ] * 6
            return
        if len(data_array) != 6:
            raise ValueError( f"invalid array size: {data_array}" )
        self.values = list( data_array )    ## copy

    def __getitem__( self, key ):
        return self.values[ key ]

    def get( self, row, col ):
        return self.values[ col + row * 2 ]

    def getDataArray(self):
        return list( self.values )


def deserialize_Transform2D( _: int, data: BytesContainer ) -> Transform2D:
    data = data.popFloat32Items(6)
    return Transform2D( data )


def serialize_Transform2D( gd_type_id: int, value: Transform2D, data: BytesContainer ):
    data.pushFlagsType( 0, gd_type_id )
    data_array = value.getDataArray()
    data.pushFloat32Items( data_array )


## =========================================================


@dataclass
class Vector4():
    w: float = 0.0
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0

    def __init__( self, data_array=None ):
        if data_array is None:
            return
        if len(data_array) != 4:
            raise ValueError( f"invalid array size: {data_array}" )
        self.w = data_array[0]
        self.x = data_array[1]
        self.y = data_array[2]
        self.z = data_array[3]

    def getDataArray(self):
        return [ self.w, self.x, self.y, self.z ]


# def deserialize_vector3( data_flags: int, data: BytesContainer ):
def deserialize_Vector4( _: int, data: BytesContainer ) -> Vector4:
    data = data.popFloat32Items(4)
    return Vector4( data )


def serialize_Vector4( gd_type_id: int, value: Vector4, data: BytesContainer ):
    data.pushFlagsType( 0, gd_type_id )
    data_array = value.getDataArray()
    data.pushFloat32Items( data_array )


## =========================================================


@dataclass
class Vector4i():
    w: int = 0
    x: int = 0
    y: int = 0
    z: int = 0

    def __init__( self, data_array=None ):
        if data_array is None:
            return
        if len(data_array) != 4:
            raise ValueError( f"invalid array size: {data_array}" )
        self.w = data_array[0]
        self.x = data_array[1]
        self.y = data_array[2]
        self.z = data_array[3]

    def getDataArray(self):
        return [ self.w, self.x, self.y, self.z ]


def deserialize_Vector4i( _: int, data: BytesContainer ) -> Vector4i:
    data = data.popInt32Items(4)
    return Vector4i( data )


def serialize_Vector4i( gd_type_id: int, value: Vector3i, data: BytesContainer ):
    data.pushFlagsType( 0, gd_type_id )
    data_array = value.getDataArray()
    data.pushInt32Items( data_array )


## =========================================================


@dataclass
class Plane():
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0
    d: float = 0.0

    def __init__( self, data_array=None ):
        if data_array is None:
            return
        if len(data_array) != 4:
            raise ValueError( f"invalid array size: {data_array}" )
        self.x = data_array[0]
        self.y = data_array[1]
        self.z = data_array[2]
        self.d = data_array[3]

    def getDataArray(self):
        return [ self.x, self.y, self.z, self.d ]


def deserialize_Plane( _: int, data: BytesContainer ) -> Plane:
    data = data.popFloat32Items(4)
    return Plane( data )


def serialize_Plane( gd_type_id: int, value: Plane, data: BytesContainer ):
    data.pushFlagsType( 0, gd_type_id )
    data_array = value.getDataArray()
    data.pushFloat32Items( data_array )


## =========================================================


@dataclass
class Quaternion():
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0
    w: float = 1.0

    def __init__( self, data_array=None ):
        if data_array is None:
            return
        if len(data_array) != 4:
            raise ValueError( f"invalid array size: {data_array}" )
        self.x = data_array[0]
        self.y = data_array[1]
        self.z = data_array[2]
        self.w = data_array[3]

    def getDataArray(self):
        return [ self.x, self.y, self.z, self.w ]


def deserialize_Quaternion( _: int, data: BytesContainer ) -> Quaternion:
    data = data.popFloat32Items(4)
    return Quaternion( data )


def serialize_Quaternion( gd_type_id: int, value: Quaternion, data: BytesContainer ):
    data.pushFlagsType( 0, gd_type_id )
    data_array = value.getDataArray()
    data.pushFloat32Items( data_array )


## =========================================================


@dataclass
class AABB():
    x_coord: float = 0.0
    y_coord: float = 0.0
    z_coord: float = 0.0
    x_size: float  = 0.0
    y_size: float  = 0.0
    z_size: float  = 0.0

    def __init__( self, data_array=None ):
        if data_array is None:
            return
        if len(data_array) != 6:
            raise ValueError( f"invalid array size: {data_array}" )
        self.x_coord = data_array[0]
        self.y_coord = data_array[1]
        self.z_coord = data_array[2]
        self.x_size  = data_array[3]
        self.y_size  = data_array[4]
        self.z_size  = data_array[5]

    def getDataArray(self):
        return [ self.x_coord, self.y_coord, self.z_coord, self.x_size, self.y_size, self.z_size ]


def deserialize_AABB( _: int, data: BytesContainer ) -> AABB:
    data = data.popFloat32Items(6)
    return AABB( data )


def serialize_AABB( gd_type_id: int, value: AABB, data: BytesContainer ):
    data.pushFlagsType( 0, gd_type_id )
    data_array = value.getDataArray()
    data.pushFloat32Items( data_array )


## =========================================================


@dataclass
class Basis():
    ## has 3 rows and 3 columns
    values: list

    def __init__( self, data_array=None ):
        if data_array is None:
            return
        if len(data_array) != 9:
            raise ValueError( f"invalid array size: {data_array}" )
        self.values = list( data_array )    ## copy

    def getDataArray(self):
        return list( self.values )


def deserialize_Basis( _: int, data: BytesContainer ) -> Basis:
    data = data.popFloat32Items(9)
    return Basis( data )


def serialize_Basis( gd_type_id: int, value: Basis, data: BytesContainer ):
    data.pushFlagsType( 0, gd_type_id )
    data_array = value.getDataArray()
    data.pushFloat32Items( data_array )


## =========================================================


@dataclass
class Transform3D():
    ## has 3 rows and 4 columns
    values: list

    def __init__( self, data_array=None ):
        if data_array is None:
            self.values: list = [ 0.0 ] * 12
            return
        if len(data_array) != 12:
            raise ValueError( f"invalid array size: {data_array}" )
        self.values = list( data_array )    ## copy

    def __getitem__( self, key ):
        return self.values[ key ]

    def get( self, row, col ):
        return self.values[ col + row * 3 ]

    def getDataArray(self):
        return list( self.values )


# def deserialize_vector3( data_flags: int, data: BytesContainer ):
def deserialize_Transform3D( _: int, data: BytesContainer ) -> Transform3D:
    data = data.popFloat32Items(12)
    return Transform3D( data )


def serialize_Transform3D( gd_type_id: int, value: Transform3D, data: BytesContainer ):
    data.pushFlagsType( 0, gd_type_id )
    data_array = value.getDataArray()
    data.pushFloat32Items( data_array )


## =========================================================


@dataclass
class Projection():
    ## has 4 rows and 4 columns
    values: list

    def __init__( self, data_array=None ):
        if data_array is None:
            self.values: list = [ 0.0 ] * 16
            return
        if len(data_array) != 16:
            raise ValueError( f"invalid array size: {data_array}" )
        self.values = list( data_array )    ## copy

    def __getitem__( self, key ):
        return self.values[ key ]

    def get( self, row, col ):
        return self.values[ col + row * 4 ]

    def getDataArray(self):
        return list( self.values )


def deserialize_Projection( _: int, data: BytesContainer ) -> Projection:
    data = data.popFloat32Items(16)
    return Projection( data )


def serialize_Projection( gd_type_id: int, value: Projection, data: BytesContainer ):
    data.pushFlagsType( 0, gd_type_id )
    data_array = value.getDataArray()
    data.pushFloat32Items( data_array )


## =========================================================


@dataclass
class Color():
    red: float   = 0.0
    green: float = 0.0
    blue: float  = 0.0
    alpha: float = 0.0

    def __init__( self, data_array=None ):
        if data_array is None:
            return
        if len(data_array) != 4:
            raise ValueError( f"invalid array size: {data_array}" )
        self.red   = data_array[0]
        self.green = data_array[1]
        self.blue  = data_array[2]
        self.alpha = data_array[3]

    def getDataArray(self):
        return [ self.red, self.green, self.blue, self.alpha ]


# def deserialize_Color( data_flags: int, data: BytesContainer ):
def deserialize_Color( _: int, data: BytesContainer ) -> Color:
    ## RGBA
    data = data.popFloat32Items(4)
    return Color( data )


def serialize_Color( gd_type_id: int, value: Color, data: BytesContainer ):
    data.pushFlagsType( 0, gd_type_id )
    ## RGBA
    data_array = value.getDataArray()
    data.pushFloat32Items( data_array )


## =========================================================


@dataclass
class StringName():
    value: str = ""


def deserialize_StringName( _: int, data: BytesContainer ) -> StringName:
    data_len = data.size()
    if data_len < 4:
        raise ValueError( f"invalid packet -- too short: {data}" )
    proper_data = data.popString()
    return StringName( proper_data )


def serialize_StringName( gd_type_id: int, value: StringName, data: BytesContainer ):
    data.pushFlagsType( 0, gd_type_id )
    raw_value = value.value
    data.pushString( raw_value )


## =========================================================


@dataclass
class NodePath():
    value: str = ""


def deserialize_NodePath( _: int, data: BytesContainer ) -> NodePath:
    data_len = data.size()
    if data_len < 4:
        raise ValueError( f"invalid packet -- too short: {data}" )
    data_header  = data.popInt32()
    header_value = data_header & 0x7FFFFFFF
    if data_header & 0x80000000 == 0:
        ## old format
        proper_data = data.popString( header_value )
        return NodePath( proper_data )
    ## new format
    raise ValueError( f"NodePath new format not supported: {data}" )

#     ## name_count = header_value
#     sub_name_count = data.popInt32()
#     is_absolute    = data.popInt32() & 1 != 0
#     return NodePath( proper_data )


def serialize_NodePath( gd_type_id: int, value: NodePath, data: BytesContainer ):
    data.pushFlagsType( 0, gd_type_id )
    raw_value = value.value
    data.pushString( raw_value )


## =========================================================


@dataclass
class RID():
    id: int = 0


def deserialize_RID( _: int, data: BytesContainer ) -> RID:
    data_len = data.size()
    if data_len < 8:
        raise ValueError( f"invalid packet -- too short: {data}" )
    rid_id = data.popInt64()
    return RID(rid_id)


def serialize_RID( gd_type_id: int, value: RID, data: BytesContainer ):
    data.pushFlagsType( 0, gd_type_id )
    data.pushInt64( value.id )


## =========================================================


# def deserialize_dict( data_flags: int, data: BytesContainer ):
def deserialize_dict( _: int, data: BytesContainer ):
    data_len = data.size()
    if data_len < 4:
        raise ValueError( f"invalid packet -- too short: {data}" )
    data_header = data.popInt32()
    list_size   = data_header & 0x7FFFFFFF
#         shared_flag = data_header & 0x80000000
    if list_size < 1:
        return {}

    proper_data = {}
    for _ in range(0, list_size):
        key_value  = deserialize_type( data )
        item_value = deserialize_type( data )
        proper_data[ key_value ] = item_value
    return proper_data


def serialize_dict( gd_type_id: int, value, data: BytesContainer ):
    data.pushFlagsType( 0, gd_type_id )
    dict_size = len( value )
#             shared_flag = 0 & 0x80000000
#             data_header = shared_flag & list_size & 0x7FFFFFFF
    data_header = dict_size & 0x7FFFFFFF
    data.pushInt32( data_header )
    for key in value:
        serialize_type( key, data )
        sub_value = value[ key ]
        serialize_type( sub_value, data )


## =========================================================

# def deserialize_list( data_flags: int, data: BytesContainer ):
def deserialize_list( _: int, data: BytesContainer ):
    data_len = data.size()
    if data_len < 4:
        raise ValueError( "invalid packet -- too short: {data}" )
    data_header = data.popInt32()
    list_size   = data_header & 0x7FFFFFFF
#         shared_flag = data_header & 0x80000000
    if list_size < 1:
        return []

    proper_data = []
    for _ in range(0, list_size):
        item_value = deserialize_type( data )
        proper_data.append( item_value )
    return proper_data


def serialize_list( gd_type_id: int, value, data: BytesContainer ):
    data.pushFlagsType( 0, gd_type_id )
    list_size = len( value )
#             shared_flag = 0 & 0x80000000
#             data_header = shared_flag & list_size & 0x7FFFFFFF
    data_header = list_size & 0x7FFFFFFF
    data.pushInt32( data_header )
    for i in range(0, list_size):
        sub_value = value[ i ]
        serialize_type( sub_value, data )


## =========================================================


@dataclass
class ByteArray():
    values: bytes = bytes()

    def __init__( self, data_array=None ):
        if data_array is None:
            return
        self.values = data_array

    def __len__(self):
        return len( self.values )

    def __getitem__( self, index ):
        return self.values[ index ]

    def toNumpy(self):
        return numpy.array( self.values )
        # return numpy.array([ point for point in self.values ])

    @staticmethod
    def fromNumpy(data_array: numpy.ndarray):
        point_list = [ int(point) for point in data_array ]
        return ByteArray( point_list )


def deserialize_ByteArray( _: int, data: BytesContainer ):
    data_len = data.size()
    if data_len < 4:
        raise ValueError( "invalid packet -- too short: {data}" )
    data_header = data.popInt32()
    list_size   = data_header
    if list_size < 1:
        return ByteArray()
    bytes_data = data.pop( list_size )
    return ByteArray( bytes_data )


def serialize_ByteArray( gd_type_id: int, value: ByteArray, data: BytesContainer ):
    data.pushFlagsType( 0, gd_type_id )
    list_size = len( value )
    data_header = list_size
    data.pushInt32( data_header )
    data.push( value.values )


## =========================================================


@dataclass
class Int32Array():
    values: List[ int ] = field(default_factory=list)

    def __init__( self, data_array=None ):
        if data_array is None:
            return
        self.values = data_array

    def __len__(self):
        return len( self.values )

    def __getitem__( self, index ):
        return self.values[ index ]

    def append( self, value ):
        self.values.append( value )

    def toNumpy(self):
        return numpy.array( self.values )
        # return numpy.array([ point for point in self.values ])

    @staticmethod
    def fromNumpy(data_array: numpy.ndarray):
        point_list = [ int(point) for point in data_array ]
        return Int32Array( point_list )


def deserialize_Int32Array( _: int, data: BytesContainer ):
    data_len = data.size()
    if data_len < 4:
        raise ValueError( "invalid packet -- too short: {data}" )
    data_header = data.popInt32()
    list_size   = data_header
    if list_size < 1:
        return Int32Array()
    data_list = data.popInt32Items( list_size )
    return Int32Array( data_list )


def serialize_Int32Array( gd_type_id: int, value: Int32Array, data: BytesContainer ):
    data.pushFlagsType( 0, gd_type_id )
    list_size = len( value )
    data_header = list_size
    data.pushInt32( data_header )
    data.pushInt32Items( value.values )


## =========================================================


@dataclass
class Int64Array():
    values: List[ int ] = field(default_factory=list)

    def __init__( self, data_array=None ):
        if data_array is None:
            return
        self.values = data_array

    def __len__(self):
        return len( self.values )

    def __getitem__( self, index ):
        return self.values[ index ]

    def append( self, value ):
        self.values.append( value )

    def toNumpy(self):
        return numpy.array( self.values )
        # return numpy.array([ point for point in self.values ])

    @staticmethod
    def fromNumpy(data_array: numpy.ndarray):
        point_list = [ int(point) for point in data_array ]
        return Int64Array( point_list )


def deserialize_Int64Array( _: int, data: BytesContainer ):
    data_len = data.size()
    if data_len < 4:
        raise ValueError( "invalid packet -- too short: {data}" )
    data_header = data.popInt32()
    list_size   = data_header
    if list_size < 1:
        return Int64Array()
    data_list = data.popInt64Items( list_size )
    return Int64Array( data_list )


def serialize_Int64Array( gd_type_id: int, value: Int64Array, data: BytesContainer ):
    data.pushFlagsType( 0, gd_type_id )
    list_size = len( value )
    data_header = list_size
    data.pushInt32( data_header )
    data.pushInt64Items( value.values )


## =========================================================


@dataclass
class Float32Array():
    values: List[ float ] = field(default_factory=list)

    def __init__( self, data_array=None ):
        if data_array is None:
            return
        self.values = data_array

    def __len__(self):
        return len( self.values )

    def __getitem__( self, index ):
        return self.values[ index ]

    def append( self, value ):
        self.values.append( value )

    def toNumpy(self):
        return numpy.array( self.values )
        # return numpy.array([ point for point in self.values ])

    @staticmethod
    def fromNumpy(data_array: numpy.ndarray):
        point_list = [ point for point in data_array ]
        return Float32Array( point_list )


def deserialize_Float32Array( _: int, data: BytesContainer ):
    data_len = data.size()
    if data_len < 4:
        raise ValueError( "invalid packet -- too short: {data}" )
    data_header = data.popInt32()
    list_size   = data_header
    if list_size < 1:
        return Float32Array()
    data_list = data.popFloat32Items( list_size )
    return Float32Array( data_list )


def serialize_Float32Array( gd_type_id: int, value: Float32Array, data: BytesContainer ):
    data.pushFlagsType( 0, gd_type_id )
    list_size = len( value )
    data_header = list_size
    data.pushInt32( data_header )
    data.pushFloat32Items( value.values )


## =========================================================


@dataclass
class Float64Array():
    values: List[ float ] = field(default_factory=list)

    def __init__( self, data_array=None ):
        if data_array is None:
            return
        self.values = data_array

    def __len__(self):
        return len( self.values )

    def __getitem__( self, index ):
        return self.values[ index ]

    def append( self, value ):
        self.values.append( value )

    def toNumpy(self):
        return numpy.array( self.values )
        # return numpy.array([ point for point in self.items ])

    @staticmethod
    def fromNumpy(data_array: numpy.ndarray):
        point_list = [ point for point in data_array ]
        return Float64Array( point_list )


def deserialize_Float64Array( _: int, data: BytesContainer ):
    data_len = data.size()
    if data_len < 4:
        raise ValueError( "invalid packet -- too short: {data}" )
    data_header = data.popInt32()
    list_size   = data_header
    if list_size < 1:
        return Float64Array()
    data_list = data.popFloat64Items( list_size )
    return Float64Array( data_list )


def serialize_Float64Array( gd_type_id: int, value: Float64Array, data: BytesContainer ):
    data.pushFlagsType( 0, gd_type_id )
    list_size = len( value )
    data_header = list_size
    data.pushInt32( data_header )
    data.pushFloat64Items( value.values )


## =========================================================


@dataclass
class StringArray():
    values: List[ str ] = field(default_factory=list)

    def __init__( self, data_array=None ):
        if data_array is None:
            self.values = []
            return
        self.values = data_array

    def __len__(self):
        return len( self.values )

    def __getitem__( self, index ):
        return self.values[ index ]

    def append( self, value ):
        self.values.append( value )


def deserialize_StringArray( _: int, data: BytesContainer ):
    data_len = data.size()
    if data_len < 4:
        raise ValueError( "invalid packet -- too short: {data}" )
    data_header = data.popInt32()
    list_size   = data_header
    if list_size < 1:
        return StringArray()

    proper_data = StringArray()
    for _ in range(0, list_size):
        val = data.popString()
        proper_data.append( val )
    return proper_data


def serialize_StringArray( gd_type_id: int, value: StringArray, data: BytesContainer ):
    data.pushFlagsType( 0, gd_type_id )
    list_size = len( value )
    data_header = list_size
    data.pushInt32( data_header )
    for i in range(0, list_size):
        item = value[ i ]
        data.pushString( item )


## =========================================================


@dataclass
class Vector2Array():
    items: List[ Tuple[float, float] ] = field(default_factory=list)        ## list of tuples(x, y)

    def __len__(self):
        return len( self.items )

    def __getitem__( self, index ):
        return self.items[ index ]

    def append( self, xcoord, ycoord ):
        self.items.append( (xcoord, ycoord) )

    def toNumpy(self):
        return numpy.array( self.items )
        # return numpy.array([ [point[0], point[1]] for point in self.items ])

    @staticmethod
    def fromNumpy(data_array: numpy.ndarray):
        point_list = [ [point[0], point[1]] for point in data_array ]
        return Vector2Array( point_list )


# def deserialize_list( data_flags: int, data: BytesContainer ):
def deserialize_Vector2Array( _: int, data: BytesContainer ):
    data_len = data.size()
    if data_len < 4:
        raise ValueError( "invalid packet -- too short: {data}" )
    data_header = data.popInt32()
    list_size   = data_header
    if list_size < 1:
        return Vector2Array()

    proper_data = Vector2Array()
    for _ in range(0, list_size):
        x_val = data.popFloat32()
        y_val = data.popFloat32()
        proper_data.append( x_val, y_val )
    return proper_data


def serialize_Vector2Array( gd_type_id: int, value: Vector2Array, data: BytesContainer ):
    data.pushFlagsType( 0, gd_type_id )
    list_size = len( value )
#             shared_flag = 0 & 0x80000000
#             data_header = shared_flag & list_size & 0x7FFFFFFF
    data_header = list_size
    data.pushInt32( data_header )
    for i in range(0, list_size):
        item = value[ i ]
        data.pushFloat32( item[0] )
        data.pushFloat32( item[1] )


## =========================================================


@dataclass
class Vector3Array():
    items: List[ Tuple[float, float, float] ] = field(default_factory=list)        ## list of tuples(x, y, z)

    def __len__(self):
        return len( self.items )

    def __getitem__( self, index ):
        return self.items[ index ]

    def append( self, xcoord, ycoord, zcoord ):
        self.items.append( (xcoord, ycoord, zcoord) )

    def toNumpy(self):
        return numpy.array( self.items )
        # return numpy.array([ [point[0], point[1], point[2]] for point in self.items ])

    @staticmethod
    def fromNumpy(data_array: numpy.ndarray):
        point_list = [ [point[0], point[1], point[2]] for point in data_array ]
        return Vector3Array( point_list )


# def deserialize_list( data_flags: int, data: BytesContainer ):
def deserialize_Vector3Array( _: int, data: BytesContainer ):
    data_len = data.size()
    if data_len < 4:
        raise ValueError( "invalid packet -- too short: {data}" )
    data_header = data.popInt32()
    list_size   = data_header
    if list_size < 1:
        return Vector3Array()

    proper_data = Vector3Array()
    for _ in range(0, list_size):
        x_val = data.popFloat32()
        y_val = data.popFloat32()
        z_val = data.popFloat32()
        proper_data.append( x_val, y_val, z_val )
    return proper_data


def serialize_Vector3Array( gd_type_id: int, value, data: BytesContainer ):
    data.pushFlagsType( 0, gd_type_id )
    list_size = len( value )
#             shared_flag = 0 & 0x80000000
#             data_header = shared_flag & list_size & 0x7FFFFFFF
    data_header = list_size
    data.pushInt32( data_header )
    for i in range(0, list_size):
        item = value[ i ]
        data.pushFloat32( item[0] )
        data.pushFloat32( item[1] )
        data.pushFloat32( item[2] )


## =========================================================


@dataclass
class ColorArray():
    items: List[ Tuple[float, float, float, float] ] = field(default_factory=list)        ## list of tuples(r, g, b, a)

    def __len__(self):
        return len( self.items )

    def __getitem__( self, index ):
        return self.items[ index ]

    def append( self, red_val, green_val, blue_val, alpha_val ):
        self.items.append( (red_val, green_val, blue_val, alpha_val) )

    def toNumpy(self):
        return numpy.array( self.items )
        # return numpy.array([ [point[0], point[1], point[2], point[3]] for point in self.items ])

    @staticmethod
    def fromNumpy(data_array: numpy.ndarray):
        point_list = [ [point[0], point[1], point[2], point[3]] for point in data_array ]
        return ColorArray( point_list )


# def deserialize_list( data_flags: int, data: BytesContainer ):
def deserialize_ColorArray( _: int, data: BytesContainer ):
    data_len = data.size()
    if data_len < 4:
        raise ValueError( "invalid packet -- too short: {data}" )
    data_header = data.popInt32()
    list_size   = data_header
    if list_size < 1:
        return ColorArray()

    proper_data = ColorArray()
    for _ in range(0, list_size):
        red_val   = data.popFloat32()
        green_val = data.popFloat32()
        blue_val  = data.popFloat32()
        alpha_val = data.popFloat32()
        proper_data.append( red_val, green_val, blue_val, alpha_val )
    return proper_data


def serialize_ColorArray( gd_type_id: int, value: ColorArray, data: BytesContainer ):
    data.pushFlagsType( 0, gd_type_id )
    list_size = len( value )
#             shared_flag = 0 & 0x80000000
#             data_header = shared_flag & list_size & 0x7FFFFFFF
    data_header = list_size
    data.pushInt32( data_header )
    for i in range(0, list_size):
        item = value[ i ]
        data.pushFloat32( item[0] )
        data.pushFloat32( item[1] )
        data.pushFloat32( item[2] )
        data.pushFloat32( item[3] )


## ======================================================================


def prepare_config_dicts( config_list, module ):
    ## calculate proper maps and validate configuration
    DESERIALIZATION_MAP: Dict[ int, Callable[[int, BytesContainer], Any] ] = {}
    SERIALIZATION_MAP: Dict[ object, Tuple[int, FunctionType] ] = {}
    # SERIALIZATION_MAP: Dict[ object, Tuple[int, Callable[[int, Any, BytesContainer], Any]] ] = {}

    for config in config_list:
        ## deserialization map
        config_gd_type: int  = config[0]
        config_py_type: type = config[1]

        if len( config ) == 4:
            deserialize_func: FunctionType = config[2]
            serialize_func: FunctionType   = config[3]
        else:
            ## find serialization/deserialization functions by name
            py_type_name = config_py_type.__name__
            deserialize_func = getattr( module, f"deserialize_{py_type_name}" )
            serialize_func   = getattr( module, f"serialize_{py_type_name}" )
#             mod_vars = vars()
#             deserialize_func = mod_vars[ f"deserialize_{py_type_name}" ]
#             serialize_func   = mod_vars[ f"serialize_{py_type_name}" ]

        if config_gd_type in DESERIALIZATION_MAP:
            raise ValueError( f"invalid CONFIG_LIST: Godot type {config_gd_type} already defined" )
        DESERIALIZATION_MAP[ config_gd_type ] = deserialize_func

        ## serialization map
        if config_py_type in SERIALIZATION_MAP:
            raise ValueError( f"invalid CONFIG_LIST: Python type {config_py_type} already defined" )
        SERIALIZATION_MAP[ config_py_type ] = ( config_gd_type, serialize_func )

    return ( DESERIALIZATION_MAP, SERIALIZATION_MAP )
