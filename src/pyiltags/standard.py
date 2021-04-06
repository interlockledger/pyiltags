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
ILTAG_VERSIO_ID = 24
ILTAG_OID_ID = 25


class ILNullTag(ILTag):
    """
    This class implements the standard tag ILTAG_NULL. 
    """
    def __init__() -> None:
        super().__init__(ILTAG_NULL_ID)
