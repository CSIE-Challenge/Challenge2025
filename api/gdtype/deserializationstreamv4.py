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

from . import binaryapiv4
from .bytescontainer import BytesContainer


_LOGGER = logging.getLogger(__name__)


class DeserializationStreamV4:

    def __init__(self, data: bytes = None):
        self.buffer = BytesContainer( data )

    def __len__(self):
        return len( self.buffer )

    def __str__(self):
        return str( self.buffer )

    def size(self):
        return len( self.buffer )

    def clear(self):
        self.buffer = BytesContainer()

    def appendData(self, data: bytes):
        self.buffer.push( data )

    ## =====================================================

    def containsMessage(self):
        check_size = binaryapiv4.check_message_size( self.buffer.data )
        return check_size >= 0

    def receive(self):
        check_size = binaryapiv4.check_message_size( self.buffer.data )
        if check_size < 0:
            return (False, check_size)
        data = self._deserialize()
        return (True, data)

    def receiveList(self):
        ret_list = []
        while binaryapiv4.check_message_size( self.buffer.data ) >= 0:
            data = self._deserialize()
            ret_list.append( data )
        return ret_list

    def _deserialize(self):
        expected_size = self.buffer.popInt32()
        message_size  = self.buffer.size()
        if message_size < expected_size:
            _LOGGER.error( "invalid packet -- packet size mismatch data size: %s", self.buffer )
            raise ValueError( f"message size mismatch: {message_size} < {expected_size} for {self.buffer}" )
        return binaryapiv4.ct.deserialize_type( self.buffer )
