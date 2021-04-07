# -*- coding: UTF-8 -*-
# BSD 3-Clause License
#
# Copyright (c) 2021, InterlockLedger
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
import pyilint
import codecs
from .base import *

# Standard tag IDs
ILTAG_NULL_ID = 0
ILTAG_BOOL_ID = 1
ILTAG_INT8_ID = 2
ILTAG_UINT8_ID = 3
ILTAG_INT16_ID = 4
ILTAG_UINT16_ID = 5
ILTAG_INT32_ID = 6
ILTAG_UINT32_ID = 7
ILTAG_INT64_ID = 8
ILTAG_UINT64_ID = 9
ILTAG_ILINT64_ID = 10
ILTAG_BINARY32_ID = 11
ILTAG_BINARY64_ID = 12
ILTAG_BINARY128_ID = 13
ILTAG_BYTE_ARRAY_ID = 16
ILTAG_STRING_ID = 17
ILTAG_BINT_ID = 18
ILTAG_BDEC_ID = 19
ILTAG_ILINT64_ARRAY_ID = 20
ILTAG_ILTAG_ARRAY_ID = 21
ILTAG_ILTAG_SEQ_ID = 22
ILTAG_RANGE_ID = 23
ILTAG_VERSION_ID = 24
ILTAG_OID_ID = 25
ILTAG_DICT_ID = 30
ILTAG_STRDICT_ID = 31

ILTAG_STANDARD_SIZES = [
    0,  # TAG_NULL
    1,  # TAG_BOOL
    1,  # TAG_INT8
    1,  # TAG_UINT8
    2,  # TAG_INT16
    2,  # TAG_UINT16
    4,  # TAG_INT32
    4,  # TAG_UINT32
    8,  # TAG_INT64
    8,  # TAG_UINT64
    9,  # TAG_ILINT64 (maximum size possible).
    4,  # TAG_BINARY32
    8,  # TAG_BINARY64
    16,  # TAG_BINARY128
    -1,  # Reserved
    -1  # Reserved
]


class ILNullTag(ILFixedSizeTag):
    """
    This class implements the standard tag ILTAG_NULL.
    """

    def __init__(self, id: int = ILTAG_NULL_ID) -> None:
        super().__init__(id, 0, True)

    def deserialize_value(self, tag_factory: ILTagFactory, tag_size: int, reader: io.IOBase) -> None:
        if tag_size != 0:
            raise ILTagCorruptedError('Corrupted null tag.')

    def serialize_value(self, writer: io.IOBase) -> None:
        pass


class ILBoolTag(ILFixedSizeTag):
    """
    This class implements the standard tag ILTAG_BOOL.
    """

    def __init__(self, value: bool = False, id: int = ILTAG_BOOL_ID) -> None:
        super().__init__(id, 1, True)
        self.value = value

    @property
    def value(self) -> bool:
        return self._value

    @value.setter
    def value(self, value: any) -> bool:
        """
        Sets the value of this tag. The final value will assume the result
        of `bool(value)`.
        """
        self._value = bool(value)

    def deserialize_value(self, tag_factory: ILTagFactory, tag_size: int, reader: io.IOBase) -> None:
        if tag_size < 1:
            raise EOFError('Unable to read the value of the tag.')
        if tag_size > 1:
            raise ILTagCorruptedError('Invalid boolean tag size.')
        v = read_bytes(1, reader)
        if v[0] == 0:
            self.value = False
        elif v[0] == 1:
            self.value = True
        else:
            raise ILTagCorruptedError('Invalid boolean value.')

    def serialize_value(self, writer: io.IOBase) -> None:
        if self.value:
            writer.write(b'\x01')
        else:
            writer.write(b'\x00')


class ILInt8Tag(ILBaseIntTag):
    def __init__(self, value: int = 0, id: int = ILTAG_INT8_ID) -> None:
        super().__init__(id, 1, True, value, True)


class ILUInt8Tag(ILBaseIntTag):
    def __init__(self, value: int = 0, id: int = ILTAG_UINT8_ID) -> None:
        super().__init__(id, 1, False, value, True)


class ILInt16Tag(ILBaseIntTag):
    def __init__(self, value: int = 0, id: int = ILTAG_INT16_ID) -> None:
        super().__init__(id, 2, True, value, True)


class ILUInt16Tag(ILBaseIntTag):
    def __init__(self, value: int = 0, id: int = ILTAG_UINT16_ID) -> None:
        super().__init__(id, 2, False, value, True)


class ILInt32Tag(ILBaseIntTag):
    def __init__(self, value: int = 0, id: int = ILTAG_INT32_ID) -> None:
        super().__init__(id, 4, True, value, True)


class ILUInt32Tag(ILBaseIntTag):
    def __init__(self, value: int = 0, id: int = ILTAG_UINT32_ID) -> None:
        super().__init__(id, 4, False, value, True)


class ILInt64Tag(ILBaseIntTag):
    def __init__(self, value: int = 0, id: int = ILTAG_INT64_ID) -> None:
        super().__init__(id, 8, True, value, True)


class ILUInt64Tag(ILBaseIntTag):
    def __init__(self, value: int = 0, id: int = ILTAG_UINT64_ID) -> None:
        super().__init__(id, 8, False, value, True)


class ILILInt64Tag(ILTag):
    def __init__(self, value: int = 0, id: int = ILTAG_ILINT64_ID) -> None:
        super().__init__(id, True)
        self.value = value

    @property
    def value(self) -> int:
        return self._value

    @value.setter
    def value(self, value: int):
        if not isinstance(value, int):
            raise TypeError('The value must be an integer.')
        assert_int_bounds(value, 8, False)
        self._value = value

    def value_size(self) -> int:
        return pyilint.ilint_size(self.value)

    def deserialize_value(self, tag_factory: ILTagFactory, tag_size: int, reader: io.IOBase) -> None:
        """
        This method behaves a little different if the tag is implicit or explicit. In the implicit
        case, the tag_size cannot be discovered without looking into the value itself. Thus, it is 
        necessary to set tag_size to any value from 1 to 9. The actual tag_size will be discovered during the
        deserialization. If the tag is explicit, the tag_size must match the actual ILInt size, otherwise the
        deserialization will fail.
        """
        if tag_size < 1 or tag_size > 9:
            raise ILTagCorruptedError('Corrupted ILInt value.')
        try:
            if self.implicit:
                self.__deserialize_value_implicit(
                    tag_factory, tag_size, reader)
            else:
                self.__deserialize_value_explicit(
                    tag_factory, tag_size, reader)
        except ValueError:
            raise ILTagCorruptedError('Invalid ILInt value.')

    def __deserialize_value_implicit(self, tag_factory: ILTagFactory, tag_size: int, reader: io.IOBase) -> None:
        header = read_bytes(1, reader)[0]
        size = pyilint.ilint_size_from_header(header)
        if size == 1:
            val = header
        else:
            if size > tag_size:
                raise ValueError()
            val, size = pyilint.ilint_decode_multibyte_core(
                header, size, read_bytes(size - 1, reader))
        self.value = val

    def __deserialize_value_explicit(self, tag_factory: ILTagFactory, tag_size: int, reader: io.IOBase) -> None:
        value, size = pyilint.ilint_decode(read_bytes(tag_size, reader))
        if size != tag_size:
            raise ILTagCorruptedError('Invalid ILInt value.')
        self._value = value

    def serialize_value(self, writer: io.IOBase) -> None:
        pyilint.ilint_encode_to_stream(self.value, writer)


class ILBinary32Tag(ILBaseFloatTag):
    def __init__(self, value: float = 0.0, id: int = ILTAG_BINARY32_ID) -> None:
        super().__init__(id, 4, value, True)


class ILBinary64Tag(ILBaseFloatTag):
    def __init__(self, value: float = 0.0, id: int = ILTAG_BINARY64_ID) -> None:
        super().__init__(id, 8, value, True)


class ILBinary128Tag(ILFixedSizeTag):
    ZERO = b'\x00' * 16

    def __init__(self, value: bytes = None, id: int = ILTAG_BINARY128_ID) -> None:
        super().__init__(id, 16, True)
        self.value = value

    @property
    def value(self) -> bytes:
        return self._value

    @value.setter
    def value(self, value: bytes):
        if value is None:
            v = ILBinary128Tag.ZERO
        elif isinstance(value, bytearray):
            v = bytes(value)
        elif isinstance(value, bytes):
            v = value
        else:
            raise TypeError(
                'The value must be an instance of bytes with 16 positions.')
        if len(v) != 16:
            raise TypeError(
                'The value must be an instance of bytes with 16 positions.')
        self._value = v

    def deserialize_value(self, tag_factory: ILTagFactory, tag_size: int, reader: io.IOBase) -> None:
        if tag_size < 16:
            raise EOFError('Unable to read the value of the tag.')
        if tag_size > 16:
            raise ILTagCorruptedError(
                'Tag too long. Expecting 16 bytes but got {tag_size}.')
        self.value = read_bytes(16, reader)

    def serialize_value(self, writer: io.IOBase) -> None:
        writer.write(self.value)


class ILByteArrayTag(ILRawTag):
    def __init__(self, value: bytes = None, id: int = ILTAG_BYTE_ARRAY_ID) -> None:
        super().__init__(id, value)


class ILStringTag(ILTag):
    """
    This class implements the tag ILTAG_STRING_ID.
    """

    def __init__(self, value: str = None, id: int = ILTAG_STRING_ID) -> None:
        """
        Creates a new instance of this class.

        Parameters:
        - `value`: The value of the tag. Must be a string or None. None is equivalent to '';
        - `id`: The id if necessary.
        """
        super().__init__(id)
        self.value = value

    @property
    def value(self) -> str:
        return self._value

    @value.setter
    def value(self, value: str):
        if value is None or value == '':
            self._value = ''
            self._utf8 = b''
        elif isinstance(value, str):
            self._value = value
            self._utf8 = codecs.encode(value, 'utf-8')
        else:
            raise TypeError('The value must be a str.')

    def value_size(self) -> int:
        return len(self.utf8)

    @property
    def utf8(self) -> bytes:
        return self._utf8

    @utf8.setter
    def utf8(self, utf8: bytes):
        if utf8 is None or utf8 == b'':
            self._value = ''
            self._utf8 = b''
        elif isinstance(utf8, bytes):
            self._value = codecs.decode(utf8, 'utf-8')
            if isinstance(utf8, bytearray):
                self._utf8 = bytes(utf8)
            else:
                self._utf8 = utf8
        else:
            raise TypeError(
                'The value must be an instance of bytes or bytearray.')

    def deserialize_value(self, tag_factory: ILTagFactory, tag_size: int, reader: io.IOBase) -> None:
        if tag_size == 0:
            self.utf8 = None
        else:
            try:
                self.utf8 = read_bytes(tag_size, reader)
            except ValueError:
                raise ILTagCorruptedError('Corrupted utf-8 string.')

    def serialize_value(self, writer: io.IOBase) -> None:
        if self.utf8 is not None:
            writer.write(self.utf8)


class ILBigIntegerTag(ILRawTag):
    def __init__(self, value: bytes = None, id: int = ILTAG_BINT_ID) -> None:
        super().__init__(id, value)


class ILBigDecimalTag(ILTag):
    def __init__(self, value: bytes = None, scale: int = 0, id: int = ILTAG_BDEC_ID) -> None:
        super().__init__(id)
        self.scale = scale
        self.value = value

    @property
    def value(self) -> bytes:
        return self._value

    @value.setter
    def value(self, value: bytes):
        if not isinstance(value, bytes):
            raise TypeError('Value must be an instance of bytes.')
        self._value = value

    @property
    def scale(self) -> int:
        return self._scale

    @scale.setter
    def scale(self, scale: int):
        assert_int_bounds(scale, 4, True)
        self._scale = scale

    def value_size(self) -> int:
        return 4 + len(self.value)

    def deserialize_value(self, tag_factory: ILTagFactory, tag_size: int, reader: io.IOBase) -> None:
        self.scale = read_int(4, True, reader)
        self.value = read_bytes(tag_size - 4, reader)

    def serialize_value(self, writer: io.IOBase) -> None:
        write_int(self.scale, 4, True, writer)
        writer.write(self.value)
