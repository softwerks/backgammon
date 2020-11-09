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

from base64 import b64decode, b64encode
from ctypes import c_uint8, c_uint64, LittleEndianStructure
from dataclasses import dataclass
from enum import IntEnum, unique
from math import log


@unique
class Player(IntEnum):
    ZERO = 0b00
    ONE = 0b01
    CENTERED = 0b11


@unique
class GameState(IntEnum):
    NOT_STARTED = 0b000
    PLAYING = 0b001
    GAME_OVER = 0b010
    RESIGNED = 0b011
    DROPPED_CUBE = 0b100


@unique
class Resign(IntEnum):
    NONE = 0b00
    SINGLE_GAME = 0b01
    GAMMON = 0b10
    BACKGAMMON = 0b11


@dataclass
class Match:
    cube_value: int
    cube_holder: Player
    player: Player
    crawford: bool
    game_state: GameState
    turn: Player
    double: bool
    resign: Resign
    dice_1: int
    dice_2: int
    length: int
    player_0_score: int
    player_1_score: int


class MatchKey(LittleEndianStructure):
    """GNU Backgammon match key.

    https://www.gnu.org/software/gnubg/manual/html_node/A-technical-description-of-the-Match-ID.html
    """

    _pack_ = 1
    _fields_ = [
        ("cube_value", c_uint8, 4),
        ("cube_holder", c_uint8, 2),
        ("player", c_uint8, 1),
        ("crawford", c_uint8, 1),
        ("game_state", c_uint64, 3),
        ("turn", c_uint64, 1),
        ("double", c_uint64, 1),
        ("resign", c_uint64, 2),
        ("dice_1", c_uint64, 3),
        ("dice_2", c_uint64, 3),
        ("length", c_uint64, 15),
        ("player_0_score", c_uint64, 15),
        ("player_1_score", c_uint64, 15),
    ]


def decode(match_id: str) -> Match:
    """Decode a match ID and return a Match.

    >>> decode("QYkqASAAIAAA")
    Match(cube_value=2, cube_holder=<Player.ZERO: 0>, player=<Player.ONE: 1>, crawford=False, game_state=<GameState.PLAYING: 1>, turn=<Player.ONE: 1>, double=False, resign=<Resign.NONE: 0>, dice_1=5, dice_2=2, length=9, player_0_score=2, player_1_score=4)
    """
    match_key: MatchKey = MatchKey.from_buffer_copy(b64decode(match_id))

    match: Match = Match(
        cube_value=2 ** match_key.cube_value,
        cube_holder=Player(match_key.cube_holder),
        player=Player(match_key.player),
        crawford=bool(match_key.crawford),
        game_state=GameState(match_key.game_state),
        turn=Player(match_key.turn),
        double=bool(match_key.double),
        resign=Resign(match_key.resign),
        dice_1=match_key.dice_1,
        dice_2=match_key.dice_2,
        length=match_key.length,
        player_0_score=match_key.player_0_score,
        player_1_score=match_key.player_1_score,
    )

    return match


def encode(match: Match) -> str:
    """Encode a Match and return a match ID.

    >>> encode(Match(cube_value=2, cube_holder=Player.ZERO, player=Player.ONE, crawford=False, game_state=GameState.PLAYING, turn=Player.ONE, double=False, resign=Resign.NONE, dice_1=5, dice_2=2, length=9, player_0_score=2, player_1_score=4))
    'QYkqASAAIAAA'
    """
    match_key = MatchKey()
    match_key.cube_value = int(log(match.cube_value, 2))
    match_key.cube_holder = match.cube_holder.value
    match_key.player = match.player.value
    match_key.crawford = int(match.crawford)
    match_key.game_state = match.game_state.value
    match_key.turn = match.turn.value
    match_key.double = int(match.double)
    match_key.resign = match.resign.value
    match_key.dice_1 = match.dice_1
    match_key.dice_2 = match.dice_2
    match_key.length = match.length
    match_key.player_0_score = match.player_0_score
    match_key.player_1_score = match.player_1_score

    match_id: str = b64encode(bytes(match_key)).decode()

    return match_id
