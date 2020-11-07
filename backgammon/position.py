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


def position_from_key(position_key: str) -> List[int]:
    """Return an internal position from a Position Key.

    >>> position_from_key('00000111110011100000111110000000000011000000011111001110000011111000000000001100')
    [0, -2, 0, 0, 0, 0, 5, 0, 3, 0, 0, 0, -5, 5, 0, 0, 0, -3, 0, -5, 0, 0, 0, 0, 2, 0, 0, 0]

    """
    checkers: List[int] = [
        sum(int(n) for n in pos) for pos in position_key.split("0")[:50]
    ]

    player_points: List[int] = checkers[:24]
    player_bar: List[int] = [checkers[24]]
    player_home: List[int] = [15 - sum(player_points)]

    opponent_points: List[int] = list(map(lambda n: -n, checkers[25:49][::-1]))
    opponent_bar: List[int] = [-checkers[49]]
    opponent_home: List[int] = [15 + sum(opponent_points)]

    merged_points: List[int] = [
        i + j for i, j in zip(player_points, opponent_points)
    ]

    position: List[
        int
    ] = opponent_bar + merged_points + player_bar + player_home + opponent_home

    return position


def key_from_position(position: List[int]) -> str:
    """Return a Position Key from an internal position.

    >>> key_from_position([0, -2, 0, 0, 0, 0, 5, 0, 3, 0, 0, 0, -5, 5, 0, 0, 0, -3, 0, -5, 0, 0, 0, 0, 2, 0, 0, 0])
    '00000111110011100000111110000000000011000000011111001110000011111000000000001100'

    """
    player_points: List[int] = list(
        map(lambda n: 0 if n < 0 else n, position[1:25])
    )
    player_bar: List[int] = [position[25]]

    opponent_points: List[int] = list(
        map(lambda n: 0 if n > 0 else -n, position[1:25][::-1])
    )
    opponent_bar: List[int] = [-position[0]]

    checkers: List[
        int
    ] = player_points + player_bar + opponent_points + opponent_bar

    position_key: str = "".join(["1" * n + "0" for n in checkers]).ljust(80, "0")

    return position_key
