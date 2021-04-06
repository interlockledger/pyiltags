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
