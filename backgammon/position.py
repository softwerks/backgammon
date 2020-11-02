# Copyright 2020 Softwerks LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Based on GNU Backgammon Position ID
# https://www.gnu.org/software/gnubg/manual/html_node/A-technical-description-of-the-Position-ID.html

import base64
import itertools
import re
import struct
from typing import List

BYTE_LEN: int = 8


def encode(position_key: str) -> str:
    """Encode a binary Position Key and return a Position ID.

    >>> encode('00000111110011100000111110000000000011000000011111001110000011111000000000001100')
    '4HPwATDgc/ABMA'

    """
    assert len(position_key) == 80, "Position Key must be exactly 80 characters."
    assert (
        re.match("^[01]+$", position_key) is not None
    ), "Position Key may only contain 0s and 1s."

    byte_array: List[str] = [
        position_key[i : i + BYTE_LEN] for i in range(0, len(position_key), BYTE_LEN)
    ]
    packed_bytes: bytes = struct.pack("10B", *[int(b[::-1], 2) for b in byte_array])
    b64: bytes = base64.b64encode(packed_bytes)
    return b64.decode()[:-2]


def decode(position_id: str) -> str:
    """Decode a Position ID and return a binary Position Key.

    >>> decode('4HPwATDgc/ABMA')
    '00000111110011100000111110000000000011000000011111001110000011111000000000001100'
    """
    b64: str = position_id + "=="
    packed_bytes: bytes = base64.b64decode(b64)
    position_key: str = "".join([format(b, "08b")[::-1] for b in packed_bytes])
    return position_key


def position_from_key(position_key: str) -> List[List[int]]:
    """Return an internal position from a Position Key.

    >>> position_from_key('00000111110011100000111110000000000011000000011111001110000011111000000000001100')
    [[0, 0, 0, 0, 0, 5, 0, 3, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0], [0, 0, 0, 0, 0, 5, 0, 3, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0]]

    """
    num_checkers: List[int] = [
        sum(int(n) for n in pos) for pos in position_key.split("0")[:50]
    ]
    position: List[List[int]] = [num_checkers[:25], num_checkers[25:]]
    return position


def key_from_position(position: List[List[int]]) -> str:
    """Return a Position Key from an internal position.

    >>> key_from_position([[0, 0, 0, 0, 0, 5, 0, 3, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0], [0, 0, 0, 0, 0, 5, 0, 3, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0]])
    '00000111110011100000111110000000000011000000011111001110000011111000000000001100'

    """
    num_checkers: List[int] = list(itertools.chain.from_iterable(position))
    position_key: str = "".join(["1"*n + "0" for n in num_checkers]).ljust(80, "0")
    return position_key
