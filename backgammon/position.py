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

import base64
from dataclasses import dataclass
import enum
import itertools
import re
import struct
from typing import List, Tuple


@dataclass
class Position:
    board_points: List[int]
    player_bar: int
    player_home: int
    opponent_bar: int
    opponent_home: int


def decode(position_id: str) -> Position:
    """Decode a position ID and return a Position.

    https://www.gnu.org/software/gnubg/manual/html_node/A-technical-description-of-the-Position-ID.html

    >>> decode('4HPwATDgc/ABMA')
    Position(board_points=[-2, 0, 0, 0, 0, 5, 0, 3, 0, 0, 0, -5, 5, 0, 0, 0, -3, 0, -5, 0, 0, 0, 0, 2], player_bar=0, player_home=0, opponent_bar=0, opponent_home=0)
    """

    def key_from_id(position_id: str) -> str:
        """Decode the the position ID and return the key (bit string)."""
        position_bytes: bytes = base64.b64decode(position_id + "==")
        position_key: str = "".join([format(b, "08b")[::-1] for b in position_bytes])
        return position_key

    def checkers_from_key(position_key: str) -> List[int]:
        """Return a list of checkers."""
        return [sum(int(n) for n in pos) for pos in position_key.split("0")[:50]]

    def merge_points(player: List[int], opponent: List[int]) -> List[int]:
        """Merge player and opponent board positions and return the combined list."""
        return [i + j for i, j in zip(player, list(map(lambda n: -n, opponent[::-1])))]

    position_key: str = key_from_id(position_id)

    checkers: List[int] = checkers_from_key(position_key)

    player_points: List[int] = checkers[:24]
    opponent_points: List[int] = checkers[25:49]
    board_points: List[int] = merge_points(player_points, opponent_points)

    player_bar: int = checkers[24]
    player_home: int = abs(15 - sum(player_points))

    opponent_bar: int = -checkers[49]
    opponent_home: int = -abs(15 - sum(player_points))

    position: Position = Position(
        board_points=board_points,
        player_bar=player_bar,
        player_home=player_home,
        opponent_bar=opponent_bar,
        opponent_home=opponent_home,
    )

    return position


def encode(position: Position) -> str:
    """Encode a Position and return a position ID.

    https://www.gnu.org/software/gnubg/manual/html_node/A-technical-description-of-the-Position-ID.html

    >>> encode(Position(board_points=[-2, 0, 0, 0, 0, 5, 0, 3, 0, 0, 0, -5, 5, 0, 0, 0, -3, 0, -5, 0, 0, 0, 0, 2], player_bar=0, player_home=0, opponent_bar=0, opponent_home=0))
    '4HPwATDgc/ABMA'

    """

    def unmerge_points(position: Position) -> Tuple[List[int], List[int]]:
        """Return player and opponent board positions starting from their respective ace points."""
        player: List[int] = list(
            map(lambda n: 0 if n < 0 else n, position.board_points,)
        )
        opponent: List[int] = list(
            map(lambda n: 0 if n > 0 else -n, position.board_points[::-1],)
        )
        return player, opponent

    def key_from_checkers(checkers: List[int]) -> str:
        """Return a position key (bit string)."""
        return "".join(["1" * n + "0" for n in checkers]).ljust(80, "0")

    def id_from_key(position_key: str) -> str:
        """Encode the position key and return the ID."""
        byte_strings: List[str] = [
            position_key[i : i + 8][::-1] for i in range(0, len(position_key), 8)
        ]
        position_bytes: bytes = struct.pack("10B", *[int(b, 2) for b in byte_strings])
        return base64.b64encode(position_bytes).decode()[:-2]

    player_points, opponent_points = unmerge_points(position)
    checkers: List[int] = player_points + [position.player_bar] + opponent_points + [
        position.opponent_bar
    ]

    position_key: str = key_from_checkers(checkers)

    position_id: str = id_from_key(position_key)

    return position_id
