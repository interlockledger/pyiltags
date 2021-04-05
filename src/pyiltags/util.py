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
from typing import Tuple


_INT_BOUNDS = {
    1: (0, 255),
    2: (0, 65535),
    4: (0, 4294967295),
    8: (0, 18446744073709551615),
    -1: (-128, 127),
    -2: (-32768, 32767),
    -4: (-2147483648, 2147483647),
    -8: (-9223372036854775808, 9223372036854775807),
}


def get_int_bounds(size: int, signed: bool) -> Tuple[int, int]:
    """
    Returns the bounds of an integer with a given size in bytes.

    Parameters:
    - `size`: Size of the integer in bytes. It must be 1, 2, 4 or 8;
    - `signed`: Determines if the integer is signed or not;

    Returns a tuple with the minimum and the maximum value allowed.
    """
    if signed:
        size = -size
    return _INT_BOUNDS[size]


def check_int_bounds(value: int, size: int, signed: bool) -> bool:
    """
    Verifies if the integer value fits inside an integer of the specified size.

    Parameters:
    - `value`: The value to be tested;
    - `size`: Size of the integer in bytes. It must be 1, 2, 4 or 8;
    - `signed`: Determines if the integer is signed or not;

    Returns True if the integer fits within the given size or false otherwise.
    """
    bounds = get_int_bounds(size, signed)
    return value >= bounds[0] and value <= bounds[1]


def assert_int_bounds(value: int, size: int, signed: bool) -> None:
    """
    Asserts that the integer value fits inside an integer of the specified size.
    It throws a `ValueError` if the value does not fit into the specified size.

    Parameters:
    - `value`: The value to be tested;
    - `size`: Size of the integer in bytes. It must be 1, 2, 4 or 8;
    - `signed`: Determines if the integer is signed or not;
    """
    bounds = get_int_bounds(size, signed)
    if value < bounds[0] or value > bounds[1]:
        raise ValueError(
            f'The value must be between {bounds[0]} and {bounds[1]}.')
