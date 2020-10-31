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
import re
import struct
from typing import List

BYTE_LEN: int = 8


def encode(position: str) -> str:
    """Encode a binary string and return a Position ID.

    >>> encode('00000111110011100000111110000000000011000000011111001110000011111000000000001100')
    '4HPwATDgc/ABMA'

    """
    assert len(position) == 80, "Binary position must be exactly 80 characters."
    assert (
        re.match("^[01]+$", position) is not None
    ), "Binary position may only contain 0s and 1s."

    byte_array: List[str] = [
        position[i : i + BYTE_LEN] for i in range(0, len(position), BYTE_LEN)
    ]
    position_bytes: bytes = struct.pack("10B", *[int(b[::-1], 2) for b in byte_array])
    position_b64: bytes = base64.b64encode(position_bytes)
    return position_b64.decode()[:-2]


def decode(position: str) -> str:
    """Decode a Position ID and return a binary string.

    >>> decode('4HPwATDgc/ABMA')
    '00000111110011100000111110000000000011000000011111001110000011111000000000001100'
    """
    position_b64: str = position + "=="
    position_bytes: bytes = base64.b64decode(position_b64)
    position_binary: str = "".join([format(b, "08b")[::-1] for b in position_bytes])
    return position_binary
