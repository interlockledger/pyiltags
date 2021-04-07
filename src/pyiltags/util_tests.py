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
from .util import *


class TestUtil(unittest.TestCase):

    def test_get_int_bounds(self):
        self.assertEqual(get_int_bounds(1, False), (0, 255))
        self.assertEqual(get_int_bounds(1, True), (-128, 127))
        self.assertEqual(get_int_bounds(2, False), (0, 65535))
        self.assertEqual(get_int_bounds(2, True), (-32768, 32767))
        self.assertEqual(get_int_bounds(4, False), (0, 4294967295))
        self.assertEqual(get_int_bounds(4, True), (-2147483648, 2147483647))
        self.assertEqual(get_int_bounds(8, False), (0, 18446744073709551615))
        self.assertEqual(get_int_bounds(8, True),
                         (-9223372036854775808, 9223372036854775807))

    def test_check_int_bounds(self):
        self.assertTrue(check_int_bounds(0, 1, False))
        self.assertTrue(check_int_bounds(255, 1, False))
        self.assertFalse(check_int_bounds(-1, 1, False))
        self.assertFalse(check_int_bounds(256, 1, False))
        self.assertTrue(check_int_bounds(-128, 1, True))
        self.assertTrue(check_int_bounds(127, 1, True))
        self.assertFalse(check_int_bounds(-129, 1, True))
        self.assertFalse(check_int_bounds(128, 1, True))

        self.assertTrue(check_int_bounds(0, 2, False))
        self.assertTrue(check_int_bounds(65535, 2, False))
        self.assertFalse(check_int_bounds(-1, 2, False))
        self.assertFalse(check_int_bounds(65536, 2, False))
        self.assertTrue(check_int_bounds(-32768, 2, True))
        self.assertTrue(check_int_bounds(32767, 2, True))
        self.assertFalse(check_int_bounds(-32769, 2, True))
        self.assertFalse(check_int_bounds(32768, 2, True))

        self.assertTrue(check_int_bounds(0, 4, False))
        self.assertTrue(check_int_bounds(4294967295, 4, False))
        self.assertFalse(check_int_bounds(-1, 4, False))
        self.assertFalse(check_int_bounds(4294967296, 4, False))
        self.assertTrue(check_int_bounds(-2147483648, 4, True))
        self.assertTrue(check_int_bounds(2147483647, 4, True))
        self.assertFalse(check_int_bounds(-2147483649, 4, True))
        self.assertFalse(check_int_bounds(2147483648, 4, True))

        self.assertTrue(check_int_bounds(0, 8, False))
        self.assertTrue(check_int_bounds(18446744073709551615, 8, False))
        self.assertFalse(check_int_bounds(-1, 8, False))
        self.assertFalse(check_int_bounds(18446744073709551616, 8, False))
        self.assertTrue(check_int_bounds(-9223372036854775808, 8, True))
        self.assertTrue(check_int_bounds(9223372036854775807, 8, True))
        self.assertFalse(check_int_bounds(-9223372036854775809, 8, True))
        self.assertFalse(check_int_bounds(9223372036854775808, 8, True))

    def test_assert_int_bounds(self):
        assert_int_bounds(0, 1, False)
        assert_int_bounds(255, 1, False)
        self.assertRaises(ValueError, assert_int_bounds, -1, 1, False)
        self.assertRaises(ValueError, assert_int_bounds, 256, 1, False)
        assert_int_bounds(-128, 1, True)
        assert_int_bounds(127, 1, True)
        self.assertRaises(ValueError, assert_int_bounds, -129, 1, True)
        self.assertRaises(ValueError, assert_int_bounds, 128, 1, True)

        assert_int_bounds(0, 2, False)
        assert_int_bounds(65535, 2, False)
        self.assertRaises(ValueError, assert_int_bounds, -1, 2, False)
        self.assertRaises(ValueError, assert_int_bounds, 65536, 2, False)
        assert_int_bounds(-32768, 2, True)
        assert_int_bounds(32767, 2, True)
        self.assertRaises(ValueError, assert_int_bounds, -32769, 2, True)
        self.assertRaises(ValueError, assert_int_bounds, 32768, 2, True)

        assert_int_bounds(0, 4, False)
        assert_int_bounds(4294967295, 4, False)
        self.assertRaises(ValueError, assert_int_bounds, -1, 4, False)
        self.assertRaises(ValueError, assert_int_bounds, 4294967296, 4, False)
        assert_int_bounds(-2147483648, 4, True)
        assert_int_bounds(2147483647, 4, True)
        self.assertRaises(ValueError, assert_int_bounds, -2147483649, 4, True)
        self.assertRaises(ValueError, assert_int_bounds, 2147483648, 4, True)

        assert_int_bounds(0, 8, False)
        assert_int_bounds(18446744073709551615, 8, False)
        self.assertRaises(ValueError, assert_int_bounds, -1, 8, False)
        self.assertRaises(ValueError, assert_int_bounds,
                          18446744073709551616, 8, False)
        assert_int_bounds(-9223372036854775808, 8, True)
        assert_int_bounds(9223372036854775807, 8, True)
        self.assertRaises(ValueError, assert_int_bounds,
                          -9223372036854775809, 8, True)
        self.assertRaises(ValueError, assert_int_bounds,
                          9223372036854775808, 8, True)


class TestRestrictListMixin(unittest.TestCase):

    class A:
        pass

    class ExampleRestrictListMixin(A, RestrictListMixin):
        def assert_value_type(self, value: T):
            if not isinstance(value, int):
                raise TypeError('Only integers are allowed.')

    def test_constructor(self):
        l = TestRestrictListMixin.ExampleRestrictListMixin()
        self.assertTrue(isinstance(l._values, list))

    def test_assert_value_type(self):
        l = RestrictListMixin()

        l.assert_value_type(None)
        l.assert_value_type(1)
        l.assert_value_type(1.0)
        l.assert_value_type('')
        l.assert_value_type([])

        l = TestRestrictListMixin.ExampleRestrictListMixin()
        l.assert_value_type(1)
        self.assertRaises(TypeError, l.assert_value_type, None)
        self.assertRaises(TypeError, l.assert_value_type, 1.0)
        self.assertRaises(TypeError, l.assert_value_type, '')
        self.assertRaises(TypeError, l.assert_value_type, [])

    def test_append(self):
        l = TestRestrictListMixin.ExampleRestrictListMixin()

        l.append(1)
        l.append(2)
        self.assertRaises(TypeError, l.append, None)
        self.assertRaises(TypeError, l.append, 1.0)
        self.assertRaises(TypeError, l.append, '')
        self.assertRaises(TypeError, l.append, [])

    def test_getset_item(self):
        l = TestRestrictListMixin.ExampleRestrictListMixin()

        l.append(1)
        l.append(2)
        self.assertEqual(1, l[0])
        self.assertEqual(2, l[1])
        for v in [1.0, '', []]:
            with self.assertRaises(TypeError):
                l[0] = v

    def test_len(self):
        l = TestRestrictListMixin.ExampleRestrictListMixin()

        self.assertEqual(0, len(l))
        l.append(1)
        self.assertEqual(1, len(l))
        l.append(2)
        self.assertEqual(2, len(l))

    def test_pop(self):
        l = TestRestrictListMixin.ExampleRestrictListMixin()

        l.append(0)
        l.append(1)
        l.append(2)
        l.append(3)

        self.assertEqual(4, len(l))
        self.assertEqual(1, l.pop(1))
        self.assertEqual(3, len(l))
        self.assertEqual(0, l[0])
        self.assertEqual(2, l[1])
        self.assertEqual(3, l[2])

        self.assertEqual(3, l.pop())
        self.assertEqual(2, len(l))
        self.assertEqual(0, l[0])
        self.assertEqual(2, l[1])

        self.assertEqual(0, l.pop(0))
        self.assertEqual(1, len(l))
        self.assertEqual(2, l[0])

    def test_clear(self):
        l = TestRestrictListMixin.ExampleRestrictListMixin()

        l.append(0)
        l.append(1)
        l.append(2)
        l.append(3)

        self.assertEqual(4, len(l))
        l.clear()
        self.assertEqual(0, len(l))

    def test_bool(self):
        l = TestRestrictListMixin.ExampleRestrictListMixin()

        self.assertFalse(bool(l))
        l.append(0)
        self.assertTrue(bool(l))
        l.append(1)
        l.clear()
        self.assertFalse(bool(l))
