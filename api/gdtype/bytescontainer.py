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
import struct
from typing import List


_LOGGER = logging.getLogger(__name__)


## mutable wrapper for bytes
class BytesContainer:

    def __init__(self, data: bytes = None):
        self.data = data
        if self.data is None:
            self.data = bytes()

    def __len__(self):
        return len( self.data )

    def size(self):
        return len( self.data )

    ## =====================================================

    ## pop front
    def pop(self, size):
        ret_data  = self.data[ :size ]
        self.data = self.data[ size: ]
        return ret_data

    ## pop int from front
    def popInt32(self) -> int:
        raw = self.pop(4)
        proper_data = int.from_bytes( raw, byteorder='little' )
        if proper_data & 0x80000000:
            ## got negative number
            neg_val = proper_data & 0x7FFFFFFF
            return -0x80000000 + neg_val
            # return proper_data & 0x7FFFFFFF | ~0x7FFFFFFF
        ## positive number
        return proper_data

    def popInt32Items(self, items_number) -> List[ int ]:
        retList = []
        for _ in range(0, items_number):
            value = self.popInt32()
            retList.append( value )
        return retList

    def popInt64(self) -> int:
        raw = self.pop(8)
        proper_data = int.from_bytes( raw, byteorder='little' )
        if proper_data & 0x8000000000000000:
            ## got negative number
            neg_val = proper_data & 0x7FFFFFFFFFFFFFFF
            return -0x8000000000000000 + neg_val
            # return proper_data & 0x7FFFFFFF | ~0x7FFFFFFF
        ## positive number
        return proper_data

    def popInt64Items(self, items_number) -> List[ int ]:
        retList = []
        for _ in range(0, items_number):
            value = self.popInt64()
            retList.append( value )
        return retList

    def popFloat32(self) -> float:
        raw = self.pop(4)
        proper_data = struct.unpack( "<f", raw )
        proper_data = proper_data[0]
        return proper_data

    def popFloat32Items(self, items_number) -> List[ float ]:
        retList = []
        for _ in range(0, items_number):
            value = self.popFloat32()
            retList.append( value )
        return retList

    def popFloat64(self) -> float:
        raw = self.pop(8)
        proper_data = struct.unpack( "<d", raw )
        proper_data = proper_data[0]
        return proper_data

    def popFloat64Items(self, items_number) -> List[ float ]:
        retList = []
        for _ in range(0, items_number):
            value = self.popFloat64()
            retList.append( value )
        return retList

    def popStringRaw(self, string_len: int) -> str:
        data_string = self.pop( string_len )
        return data_string.decode("utf-8")

    def popString(self, string_len: int = -1 ) -> str:
        if string_len < 0:
            string_len = self.popInt32()
        if string_len < 1:
            return ""
        proper_data = self. popStringRaw( string_len )
        remaining = string_len % 4
        if remaining > 0:
            padding = 4 - remaining
            ## pop remaining padding (zero bytes)
            self.pop( padding )
        return proper_data

    ## pop from front
    def popFlagsType(self) -> int:
        raw = self.popInt32()
        data_type  = raw & 0xFF
        data_flags = (raw >> 16) & 0xFF
        return ( data_flags, data_type )

    ## =====================================================

    def push( self, value: bytes ):
        self.data = self.data + value

    def pushZeros( self, number: int ):
        if number < 1:
            return
        zeros = bytes()
        for _ in range( 0, number ):
            zeros = zeros + b'\x00'
        self.data = self.data + zeros

    ## push back value
    def pushInt32( self, value: int ):
        if value & 0x80000000:
            ## got negative number
            pos_val = value & 0x7FFFFFFF
            value = 0x80000000 + pos_val
        raw = value.to_bytes( 4, byteorder='little' )
        self.push( raw )

    def pushInt32Items(self, value_array: List[int] ):
        for item in value_array:
            self.pushInt32( item )

    ## push back value
    def pushInt64( self, value: int ):
        if value & 0x8000000000000000:
            ## got negative number
            pos_val = value & 0x7FFFFFFFFFFFFFFF
            value = 0x8000000000000000 + pos_val
        raw = value.to_bytes( 8, byteorder='little' )
        self.push( raw )

    def pushInt64Items(self, value_array: List[int] ):
        for item in value_array:
            self.pushInt64( item )

    def pushFloat32(self, value: float):
        raw = struct.pack( "<f", value )
        self.push( raw )

    def pushFloat32Items(self, value_array: List[float] ):
        for item in value_array:
            self.pushFloat32( item )

    def pushFloat64(self, value: float):
        raw = struct.pack( "<d", value )
        self.push( raw )

    def pushFloat64Items(self, value_array: List[float] ):
        for item in value_array:
            self.pushFloat64( item )

    def pushStringRaw(self, value: str):
        raw = value.encode("utf-8")
        self.push( raw )

    def pushString(self, value: str):
        str_len = len( value )
        self.pushInt32( str_len )
        self.pushStringRaw( value )
        remaining = str_len % 4
        if remaining > 0:
            padding = 4 - remaining
            self.pushZeros( padding )

    ## push back value
    def pushFlagsType( self, flags: int, data_type: int ):
        value = ((flags & 0xFF) << 16) | ( data_type & 0xFF )
        self.pushInt32( value )

    ## =====================================================

    def __str__(self):
        return str( self.data )
