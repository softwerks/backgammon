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

# Position ID
# https://www.gnu.org/software/gnubg/manual/html_node/A-technical-description-of-the-Position-ID.html
# Official documentation is inaccurate. Position key (binary string) starts from the opponent's ace point. See:
# https://lists.gnu.org/archive/html/bug-gnubg/2005-01/msg00081.html
# https://lists.gnu.org/archive/html/bug-gnubg/2013-01/msg00010.html

import base64
import dataclasses
import struct
from typing import List, NamedTuple, Optional, Tuple


@dataclasses.dataclass(frozen=True)
class Position:
    board_points: Tuple[int, ...]
    player_bar: int
    player_off: int
    opponent_bar: int
    opponent_off: int


class Move(NamedTuple):
    pips: int
    source: Optional[int]
    destination: Optional[int]


class Play(NamedTuple):
    moves: Tuple[Move, ...]
    board: Position


def apply_move(board: Position, move: Move) -> Position:
    """Apply a move and return a new position."""
    board_points: List[int] = list(board.board_points)
    player_bar: int = board.player_bar
    player_off: int = board.player_off
    opponent_bar: int = board.opponent_bar
    opponent_off: int = board.opponent_off

    if move.source is None:
        player_bar -= 1
    else:
        board_points[move.source - 1] -= 1

    if move.destination is None:
        player_off += 1
    else:
        hit: bool = True if board_points[move.destination - 1] == -1 else False
        if hit:
            board_points[move.destination - 1] = 1
            opponent_bar += 1
        else:
            board_points[move.destination - 1] += 1

    return Position(
        tuple(board_points), player_bar, player_off, opponent_bar, opponent_off
    )


def decode(position_id: str) -> Position:
    """Decode a position ID and return a Position.

    >>> decode('4HPwATDgc/ABMA')
    Position(board_points=(-2, 0, 0, 0, 0, 5, 0, 3, 0, 0, 0, -5, 5, 0, 0, 0, -3, 0, -5, 0, 0, 0, 0, 2), player_bar=0, player_off=0, opponent_bar=0, opponent_off=0)
    """

    def key_from_id(position_id: str) -> str:
        """Decode the the position ID and return the key (bit string)."""
        position_bytes: bytes = base64.b64decode(position_id + "==")
        position_key: str = "".join([format(b, "08b")[::-1] for b in position_bytes])
        return position_key

    def checkers_from_key(position_key: str) -> Tuple[int, ...]:
        """Return a list of checkers."""
        return tuple(sum(int(n) for n in pos) for pos in position_key.split("0")[:50])

    def merge_points(
        player: Tuple[int, ...], opponent: Tuple[int, ...]
    ) -> Tuple[int, ...]:
        """Merge player and opponent board positions and return the combined points."""
        return tuple(
            i + j for i, j in zip(player, tuple(map(lambda n: -n, opponent[::-1])))
        )

    position_key: str = key_from_id(position_id)

    checkers: Tuple[int, ...] = checkers_from_key(position_key)

    player_points: Tuple[int, ...] = checkers[25:49]
    opponent_points: Tuple[int, ...] = checkers[:24]
    board_points: Tuple[int, ...] = merge_points(player_points, opponent_points)

    player_bar: int = checkers[49]
    player_off: int = abs(15 - sum(player_points))

    opponent_bar: int = -checkers[24]
    opponent_off: int = -abs(15 - sum(opponent_points))

    position: Position = Position(
        board_points=board_points,
        player_bar=player_bar,
        player_off=player_off,
        opponent_bar=opponent_bar,
        opponent_off=opponent_off,
    )

    return position


def encode(position: Position) -> str:
    """Encode a Position and return a position ID.

    >>> encode(Position(board_points=(-2, 0, 0, 0, 0, 5, 0, 3, 0, 0, 0, -5, 5, 0, 0, 0, -3, 0, -5, 0, 0, 0, 0, 2), player_bar=0, player_off=0, opponent_bar=0, opponent_off=0))
    '4HPwATDgc/ABMA'

    """

    def unmerge_points(position: Position) -> Tuple[Tuple[int, ...], Tuple[int, ...]]:
        """Return player and opponent board positions starting from their respective ace points."""
        player: Tuple[int, ...] = tuple(
            map(lambda n: 0 if n < 0 else n, position.board_points,)
        )
        opponent: Tuple[int, ...] = tuple(
            map(lambda n: 0 if n > 0 else -n, position.board_points[::-1],)
        )
        return player, opponent

    def key_from_checkers(checkers: Tuple[int, ...]) -> str:
        """Return a position key (bit string)."""
        return "".join("1" * n + "0" for n in checkers).ljust(80, "0")

    def id_from_key(position_key: str) -> str:
        """Encode the position key and return the ID."""
        byte_strings: Tuple[str, ...] = tuple(
            position_key[i : i + 8][::-1] for i in range(0, len(position_key), 8)
        )
        position_bytes: bytes = struct.pack("10B", *(int(b, 2) for b in byte_strings))
        return base64.b64encode(position_bytes).decode()[:-2]

    player_points, opponent_points = unmerge_points(position)
    checkers: Tuple[int, ...] = opponent_points + (
        position.opponent_bar,
    ) + player_points + (position.player_bar,)

    position_key: str = key_from_checkers(checkers)

    position_id: str = id_from_key(position_key)

    return position_id
