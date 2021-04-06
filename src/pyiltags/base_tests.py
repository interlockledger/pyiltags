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
import unittest
from unittest.mock import MagicMock

from pyilint import ilint_encode_to_stream, ilint_size
from .base import *


class TestBaseFunctions(unittest.TestCase):

    def test_iltags_assert_valid_id(self):
        iltags_assert_valid_id(0)
        iltags_assert_valid_id(2**64 - 1)
        self.assertRaises(ValueError, iltags_assert_valid_id, -1)
        self.assertRaises(ValueError, iltags_assert_valid_id, 2**64)

    def test_iltags_is_implicit(self):
        self.assertRaises(ValueError, iltags_is_implicit, -1)
        self.assertRaises(ValueError, iltags_is_implicit, 2**64)
        for id in range(16):
            self.assertTrue(iltags_is_implicit(id))
        self.assertFalse(iltags_is_implicit(16))
        self.assertFalse(iltags_is_implicit(32))
        self.assertFalse(iltags_is_implicit(64))

    def test_iltags_is_standard(self):
        self.assertRaises(ValueError, iltags_is_standard, -1)
        self.assertRaises(ValueError, iltags_is_standard, 2**64)
        for id in range(32):
            self.assertTrue(iltags_is_standard(id))
        self.assertFalse(iltags_is_standard(32))
        self.assertFalse(iltags_is_standard(64))


class TestILTagFactory(unittest.TestCase):

    def test_constructor(self):
        c = ILTagFactory()
        self.assertFalse(c.strict)
        self.assertRaises(NotImplementedError, c.create, 10)
        self.assertRaises(NotImplementedError, c.deserialize, io.BytesIO())

        c = ILTagFactory(True)
        self.assertTrue(c.strict)
        self.assertRaises(NotImplementedError, c.create, 10)
        self.assertRaises(NotImplementedError, c.deserialize, io.BytesIO())

        c = ILTagFactory(False)
        self.assertFalse(c.strict)
        self.assertRaises(NotImplementedError, c.create, 10)
        self.assertRaises(NotImplementedError, c.deserialize, io.BytesIO())


class TestILTag(unittest.TestCase):

    def test_constructor(self):
        t = ILTag(0)
        self.assertEqual(t.id, 0)

        t = ILTag(2**64 - 1)
        self.assertEqual(t.id, 2**64 - 1)

        self.assertRaises(ValueError, ILTag, -1)
        self.assertRaises(ValueError, ILTag, 2**64)

    def test_implicit(self):
        for id in range(16):
            t = ILTag(id)
            self.assertTrue(t.implicit)
        t = ILTag(16)
        self.assertFalse(t.implicit)

    def test_standard(self):
        for id in range(32):
            t = ILTag(id)
            self.assertTrue(t.standard)
        t = ILTag(32)
        self.assertFalse(t.standard)

    def test_value_size(self):
        t = ILTag(0)
        self.assertRaises(NotImplementedError, t.value_size)

    def test_tag_size(self):
        for id in range(16):
            t = ILTag(id)
            t.value_size = MagicMock(return_value=id)
            size = ilint_size(id) + id
            self.assertEqual(t.tag_size(), size)
            t.value_size.assert_called_once()
            self.assertEqual(len(t), size)

        for id in [16, 256, 1231231]:
            t = ILTag(id)
            t.value_size = MagicMock(return_value=id)
            size = ilint_size(id) + ilint_size(id) + id
            self.assertEqual(t.tag_size(), size)
            t.value_size.assert_called_once()
            self.assertEqual(len(t), size)

    def test_deserialize_value(self):
        t = ILTag(0)
        self.assertRaises(NotImplementedError, t.deserialize_value,
                          ILTagFactory(), 0, io.BytesIO())

    def test_serialize_value(self):
        t = ILTag(0)
        self.assertRaises(NotImplementedError, t.serialize_value, io.BytesIO())

    def test_serialize(self):
        class DummyILTag(ILTag):
            def value_size(self) -> int:
                return 4

            def serialize_value(self, writer: io.IOBase) -> None:
                writer.write(b'1234')

        # Normal tag with no payload
        t = DummyILTag(65535)
        writer = io.BytesIO()
        t.serialize(writer)

        exp = io.BytesIO()
        ilint_encode_to_stream(65535, exp)
        ilint_encode_to_stream(4, exp)
        exp.write(b'1234')
        exp.seek(0)
        writer.seek(0)
        self.assertEqual(exp.read(), writer.read())

        # Implicit
        t = DummyILTag(1)
        writer = io.BytesIO()
        t.serialize(writer)

        exp = io.BytesIO()
        ilint_encode_to_stream(1, exp)
        exp.write(b'1234')
        exp.seek(0)
        writer.seek(0)
        self.assertEqual(exp.read(), writer.read())
