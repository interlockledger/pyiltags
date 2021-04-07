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
from typing import Callable
import unittest
from .standard import *


class TestILTagIds(unittest.TestCase):

    def test_standard_ids(self):
        self.assertEqual(ILTAG_NULL_ID, 0)
        self.assertEqual(ILTAG_BOOL_ID, 1)
        self.assertEqual(ILTAG_INT8_ID, 2)
        self.assertEqual(ILTAG_UINT8_ID, 3)
        self.assertEqual(ILTAG_INT16_ID, 4)
        self.assertEqual(ILTAG_UINT16_ID, 5)
        self.assertEqual(ILTAG_INT32_ID, 6)
        self.assertEqual(ILTAG_UINT32_ID, 7)
        self.assertEqual(ILTAG_INT64_ID, 8)
        self.assertEqual(ILTAG_UINT64_ID, 9)
        self.assertEqual(ILTAG_ILINT64_ID, 10)
        self.assertEqual(ILTAG_BINARY32_ID, 11)
        self.assertEqual(ILTAG_BINARY64_ID, 12)
        self.assertEqual(ILTAG_BINARY128_ID, 13)
        self.assertEqual(ILTAG_BYTE_ARRAY_ID, 16)
        self.assertEqual(ILTAG_STRING_ID, 17)
        self.assertEqual(ILTAG_BINT_ID, 18)
        self.assertEqual(ILTAG_BDEC_ID, 19)
        self.assertEqual(ILTAG_ILINT64_ARRAY_ID, 20)
        self.assertEqual(ILTAG_ILTAG_ARRAY_ID, 21)
        self.assertEqual(ILTAG_ILTAG_SEQ_ID, 22)
        self.assertEqual(ILTAG_RANGE_ID, 23)
        self.assertEqual(ILTAG_VERSION_ID, 24)
        self.assertEqual(ILTAG_OID_ID, 25)
        self.assertEqual(ILTAG_DICT_ID, 30)
        self.assertEqual(ILTAG_STRDICT_ID, 31)


class TestILNullTag(unittest.TestCase):

    def test_contructor(self):
        t = ILNullTag()
        self.assertEqual(ILTAG_NULL_ID, t.id)
        self.assertEqual(0, t.value_size())

        t = ILNullTag(123)
        self.assertEqual(123, t.id)
        self.assertEqual(0, t.value_size())

    def test_deserialize_value(self):
        t = ILNullTag()
        reader = io.BytesIO(b'123456')
        t.deserialize_value(None, 0, reader)
        self.assertEqual(0, reader.tell())
        self.assertRaises(ILTagCorruptedError,
                          t.deserialize_value, None, 1, reader)

    def test_serialize_value(self):
        t = ILNullTag()
        writer = io.BytesIO()
        t.serialize_value(writer)
        self.assertEqual(0, writer.tell())


class TestILBoolTag(unittest.TestCase):

    def test_contructor(self):
        t = ILBoolTag()
        self.assertEqual(ILTAG_BOOL_ID, t.id)
        self.assertEqual(1, t.value_size())
        self.assertFalse(t.value)

        t = ILBoolTag(False)
        self.assertEqual(ILTAG_BOOL_ID, t.id)
        self.assertEqual(1, t.value_size())
        self.assertFalse(t.value)

        t = ILBoolTag(True)
        self.assertEqual(ILTAG_BOOL_ID, t.id)
        self.assertEqual(1, t.value_size())
        self.assertTrue(t.value)

        t = ILBoolTag(False, 123123)
        self.assertEqual(123123, t.id)
        self.assertEqual(1, t.value_size())
        self.assertFalse(t.value)

        t = ILBoolTag(True, 123123)
        self.assertEqual(123123, t.id)
        self.assertEqual(1, t.value_size())
        self.assertTrue(t.value)

    def test_value(self):
        t = ILBoolTag()

        for v in [False, 0, None, b'', '', []]:
            t.value = v
            self.assertFalse(t.value)
        for v in [True, 1, 1.0, b'x', 'z', [1]]:
            t.value = v
            self.assertTrue(t.value)

    def test_deserialize_value(self):
        t = ILBoolTag(True)

        t.deserialize_value(None, 1, io.BytesIO(b'\x00'))
        self.assertFalse(t.value)

        t.deserialize_value(None, 1, io.BytesIO(b'\x01'))
        self.assertTrue(t.value)

        self.assertRaises(EOFError,
                          t.deserialize_value, None, 0, io.BytesIO(b'\x00'))
        self.assertRaises(ILTagCorruptedError,
                          t.deserialize_value, None, 2, io.BytesIO(b'\x0001'))
        self.assertRaises(ILTagCorruptedError,
                          t.deserialize_value, None, 1, io.BytesIO(b'\x02'))

    def test_serialize_value(self):
        t = ILBoolTag()

        writer = io.BytesIO()
        t.serialize_value(writer)
        self.assertEqual(1, writer.tell())
        writer.seek(0)
        self.assertEqual(b'\x00', writer.read())

        t.value = True
        writer = io.BytesIO()
        t.serialize_value(writer)
        self.assertEqual(1, writer.tell())
        writer.seek(0)
        self.assertEqual(b'\x01', writer.read())


class BaseTestILIntTag(unittest.TestCase):
    def constructor_core(self, tag_class: Callable, exp_size: int, default_id: int, signed: bool):
        t = tag_class()
        self.assertEqual(default_id, t.id)
        self.assertEqual(exp_size, t.value_size())
        self.assertEqual(0, t.value)
        self.assertEqual(signed, t.signed)

        t = tag_class(123)
        self.assertEqual(default_id, t.id)
        self.assertEqual(exp_size, t.value_size())
        self.assertEqual(123, t.value)
        self.assertEqual(signed, t.signed)

        t = tag_class(123, 456)
        self.assertEqual(456, t.id)
        self.assertEqual(exp_size, t.value_size())
        self.assertEqual(123, t.value)
        self.assertEqual(signed, t.signed)

    def test_constructor(self):
        self.constructor_core(ILInt8Tag, 1, ILTAG_INT8_ID, True)
        self.constructor_core(ILUInt8Tag, 1, ILTAG_UINT8_ID, False)
        self.constructor_core(ILInt16Tag, 2, ILTAG_INT16_ID, True)
        self.constructor_core(ILUInt16Tag, 2, ILTAG_UINT16_ID, False)
        self.constructor_core(ILInt32Tag, 4, ILTAG_INT32_ID, True)
        self.constructor_core(ILUInt32Tag, 4, ILTAG_UINT32_ID, False)
        self.constructor_core(ILInt64Tag, 8, ILTAG_INT64_ID, True)
        self.constructor_core(ILUInt64Tag, 8, ILTAG_UINT64_ID, False)


class TestILILInt64Tag(unittest.TestCase):

    def test_constructor(self):
        t = ILILInt64Tag()
        self.assertEqual(ILTAG_ILINT64_ID, t.id)
        self.assertEqual(0, t.value)

        t = ILILInt64Tag(123)
        self.assertEqual(ILTAG_ILINT64_ID, t.id)
        self.assertEqual(123, t.value)

        t = ILILInt64Tag(123, 456)
        self.assertEqual(456, t.id)
        self.assertEqual(123, t.value)

        self.assertRaises(ValueError, ILILInt64Tag, -1)
        self.assertRaises(ValueError, ILILInt64Tag, 2**64)
        self.assertRaises(TypeError, ILILInt64Tag, '1')
        self.assertRaises(TypeError, ILILInt64Tag, 1.0)

    def test_value(self):
        t = ILILInt64Tag()

        t.value = 0
        self.assertEqual(0, t.value)

        t.value = 2**64 - 1
        self.assertEqual(2**64 - 1, t.value)

        for v in ['', '1', b'123', 1.0]:
            with self.assertRaises(TypeError):
                t.value = v
        for v in [-1, 2**64]:
            with self.assertRaises(ValueError):
                t.value = v

    def test_value_size(self):

        for v in [0, 0xFF, 0xFFFF, 0xFFFFFF, 0xFFFFFFFF, 0xFFFFFFFF,
                  0xFFFFFFFFFF, 0xFFFFFFFFFFFF,
                  0xFFFFFFFFFFFFFF, 0xFFFFFFFFFFFFFFFF]:
            t = ILILInt64Tag(v)
            self.assertEqual(pyilint.ilint_size(t.value), t.value_size())

    def test_deserialize_value_implicit(self):

        for v in [0, 0xFF, 0xFFFF, 0xFFFFFF, 0xFFFFFFFF, 0xFFFFFFFF,
                  0xFFFFFFFFFF, 0xFFFFFFFFFFFF,
                  0xFFFFFFFFFFFFFF, 0xFFFFFFFFFFFFFFFF]:
            t = ILILInt64Tag()
            val = bytearray()
            size = pyilint.ilint_encode(v, val)
            reader = io.BytesIO(val)
            t.deserialize_value(None, size, reader)
            self.assertEqual(size, reader.tell())
            self.assertEqual(v, t.value)

        t = ILILInt64Tag()
        reader = io.BytesIO(bytes.fromhex('FFFFFFFFFFFFFFFFFF'))
        self.assertRaises(ILTagCorruptedError,
                          t.deserialize_value, None, 9, reader)
        reader.seek(0)
        self.assertRaises(ILTagCorruptedError,
                          t.deserialize_value, None, 0, reader)
        reader.seek(0)
        self.assertRaises(ILTagCorruptedError,
                          t.deserialize_value, None, 10, reader)
        reader.seek(0)
        self.assertRaises(ILTagCorruptedError,
                          t.deserialize_value, None, 8, reader)

    def test_deserialize_value_explicit(self):

        for v in [0, 0xFF, 0xFFFF, 0xFFFFFF, 0xFFFFFFFF, 0xFFFFFFFF,
                  0xFFFFFFFFFF, 0xFFFFFFFFFFFF,
                  0xFFFFFFFFFFFFFF, 0xFFFFFFFFFFFFFFFF]:
            t = ILILInt64Tag(id=1234)
            val = bytearray()
            size = pyilint.ilint_encode(v, val)
            reader = io.BytesIO(val)
            t.deserialize_value(None, size, reader)
            self.assertEqual(size, reader.tell())
            self.assertEqual(v, t.value)

        t = ILILInt64Tag(id=1234)
        reader = io.BytesIO(bytes.fromhex('FFFFFFFFFFFFFFFFFF00'))
        self.assertRaises(ILTagCorruptedError,
                          t.deserialize_value, None, 9, reader)
        reader.seek(0)
        self.assertRaises(ILTagCorruptedError,
                          t.deserialize_value, None, 0, reader)
        reader.seek(0)
        self.assertRaises(ILTagCorruptedError,
                          t.deserialize_value, None, 10, reader)
        reader.seek(0)
        self.assertRaises(ILTagCorruptedError,
                          t.deserialize_value, None, 8, reader)

    def test_serialize_value(self):

        for v in [0, 0xFF, 0xFFFF, 0xFFFFFF, 0xFFFFFFFF, 0xFFFFFFFF,
                  0xFFFFFFFFFF, 0xFFFFFFFFFFFF,
                  0xFFFFFFFFFFFFFF, 0xFFFFFFFFFFFFFFFF]:
            t = ILILInt64Tag(v)

            val = bytearray()
            size = pyilint.ilint_encode(v, val)

            writer = io.BytesIO()
            t.serialize_value(writer)
            self.assertEqual(size, writer.tell())
            writer.seek(0)
            self.assertEqual(val, writer.read())


class TestILByteArrayTag(unittest.TestCase):

    def test_constructor(self):
        t = ILByteArrayTag()
        self.assertEqual(ILTAG_BYTE_ARRAY_ID, t.id)
        self.assertEqual(None, t.value)

        paylod = b'1234'
        t = ILByteArrayTag(paylod)
        self.assertEqual(ILTAG_BYTE_ARRAY_ID, t.id)
        self.assertEqual(paylod, t.value)

        t = ILByteArrayTag(paylod, 1234)
        self.assertEqual(1234, t.id)
        self.assertEqual(paylod, t.value)
