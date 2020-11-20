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
import ctypes
import dataclasses
import enum
import math
from typing import Tuple


@enum.unique
class Player(enum.IntEnum):
    ZERO = 0b00
    ONE = 0b01
    CENTERED = 0b11


@enum.unique
class GameState(enum.IntEnum):
    NOT_STARTED = 0b000
    PLAYING = 0b001
    GAME_OVER = 0b010
    RESIGNED = 0b011
    DROPPED_CUBE = 0b100


@enum.unique
class Resign(enum.IntEnum):
    NONE = 0b00
    SINGLE_GAME = 0b01
    GAMMON = 0b10
    BACKGAMMON = 0b11


class MatchKey(ctypes.LittleEndianStructure):
    """GNU Backgammon match key.

    https://www.gnu.org/software/gnubg/manual/html_node/A-technical-description-of-the-Match-ID.html
    """

    _pack_ = 1
    _fields_ = [
        ("cube_value", ctypes.c_uint8, 4),
        ("cube_holder", ctypes.c_uint8, 2),
        ("player", ctypes.c_uint8, 1),
        ("crawford", ctypes.c_uint8, 1),
        ("game_state", ctypes.c_uint64, 3),
        ("turn", ctypes.c_uint64, 1),
        ("double", ctypes.c_uint64, 1),
        ("resign", ctypes.c_uint64, 2),
        ("dice_1", ctypes.c_uint64, 3),
        ("dice_2", ctypes.c_uint64, 3),
        ("length", ctypes.c_uint64, 15),
        ("player_0_score", ctypes.c_uint64, 15),
        ("player_1_score", ctypes.c_uint64, 15),
    ]


@dataclasses.dataclass
class Match:
    cube_value: int
    cube_holder: Player
    player: Player
    crawford: bool
    game_state: GameState
    turn: Player
    double: bool
    resign: Resign
    dice: Tuple[int, int]
    length: int
    player_0_score: int
    player_1_score: int

    @staticmethod
    def decode(match_id: str) -> "Match":
        """Decode a match ID and return a Match.

        >>> Match.decode("QYkqASAAIAAA")
        Match(cube_value=2, cube_holder=<Player.ZERO: 0>, player=<Player.ONE: 1>, crawford=False, game_state=<GameState.PLAYING: 1>, turn=<Player.ONE: 1>, double=False, resign=<Resign.NONE: 0>, dice=(5, 2), length=9, player_0_score=2, player_1_score=4)
        """
        match_key: MatchKey = MatchKey.from_buffer_copy(base64.b64decode(match_id))

        return Match(
            cube_value=2 ** match_key.cube_value,
            cube_holder=Player(match_key.cube_holder),
            player=Player(match_key.player),
            crawford=bool(match_key.crawford),
            game_state=GameState(match_key.game_state),
            turn=Player(match_key.turn),
            double=bool(match_key.double),
            resign=Resign(match_key.resign),
            dice=(match_key.dice_1, match_key.dice_2),
            length=match_key.length,
            player_0_score=match_key.player_0_score,
            player_1_score=match_key.player_1_score,
        )

    def encode(self) -> str:
        """Encode the match and return a match ID.

        >>> match = Match(cube_value=2, cube_holder=Player.ZERO, player=Player.ONE, crawford=False, game_state=GameState.PLAYING, turn=Player.ONE, double=False, resign=Resign.NONE, dice=(5, 2), length=9, player_0_score=2, player_1_score=4)
        >>> match.encode()
        'QYkqASAAIAAA'
        """
        match_key = MatchKey()
        match_key.cube_value = int(math.log(self.cube_value, 2))
        match_key.cube_holder = self.cube_holder.value
        match_key.player = self.player.value
        match_key.crawford = int(self.crawford)
        match_key.game_state = self.game_state.value
        match_key.turn = self.turn.value
        match_key.double = int(self.double)
        match_key.resign = self.resign.value
        match_key.dice_1 = self.dice[0]
        match_key.dice_2 = self.dice[1]
        match_key.length = self.length
        match_key.player_0_score = self.player_0_score
        match_key.player_1_score = self.player_1_score

        match_id: str = base64.b64encode(bytes(match_key)).decode()

        return match_id
