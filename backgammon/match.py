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
import dataclasses
import enum
import math
import struct
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

    def swap_players(self) -> "Match":
        self.player = self.turn = (
            Player.ZERO if self.player is Player.ONE else Player.ONE
        )

        return self

    def swap_turn(self) -> "Match":
        self.turn = Player.ZERO if self.turn is Player.ONE else Player.ONE

        return self

    def reset_dice(self) -> "Match":
        self.dice = (0, 0)

        return self

    def reset_cube(self) -> "Match":
        self.cube_holder = Player.CENTERED
        self.cube_value = 1

        return self

    def drop_cube(self) -> "Match":
        if self.player is Player.ZERO:
            self.player_0_score += self.cube_value
        else:
            self.player_1_score += self.cube_value

        self.double = False

        if self.player_0_score >= self.length or self.player_1_score >= self.length:
            self.game_state = GameState.DROPPED_CUBE

        return self

    def update_score(self, multiplier: int) -> "Match":
        points: int = self.cube_value * multiplier

        self.crawford = False

        if self.turn is Player.ZERO:
            self.player_0_score += points
            if (
                self.length - self.player_0_score == 1
                and self.length - self.player_1_score > 1
            ):
                self.crawford = True
        else:
            self.player_1_score += points
            if (
                self.length - self.player_1_score == 1
                and self.length - self.player_0_score > 1
            ):
                self.crawford = True

        self.double = False

        if self.player_0_score >= self.length or self.player_1_score >= self.length:
            self.game_state = GameState.GAME_OVER

        return self

    def encode(self) -> str:
        """Encode the match and return a match ID.

        >>> match = Match(cube_value=2, cube_holder=Player.ZERO, player=Player.ONE, crawford=False, game_state=GameState.PLAYING, turn=Player.ONE, double=False, resign=Resign.NONE, dice=(5, 2), length=9, player_0_score=2, player_1_score=4)
        >>> match.encode()
        'QYkqASAAIAAA'
        """
        match_key: str = "".join(
            (
                f"{int(math.log(self.cube_value, 2)):04b}"[::-1],
                f"{self.cube_holder.value:02b}"[::-1],
                f"{self.player.value:b}",
                f"{self.crawford:b}",
                f"{self.game_state.value:03b}"[::-1],
                f"{self.turn:b}",
                f"{self.double:b}",
                f"{self.resign.value:02b}"[::-1],
                f"{self.dice[0]:03b}"[::-1],
                f"{self.dice[1]:03b}"[::-1],
                f"{self.length:015b}"[::-1],
                f"{self.player_0_score:015b}"[::-1],
                f"{self.player_1_score:015b}"[::-1],
            )
        )
        byte_strings: Tuple[str, ...] = tuple(
            match_key[i : i + 8][::-1] for i in range(0, len(match_key), 8)
        )
        match_bytes: bytes = struct.pack("9B", *(int(b, 2) for b in byte_strings))
        return base64.b64encode(bytes(match_bytes)).decode()


def decode(match_id: str) -> Match:
    """Decode a match ID and return a Match.

    >>> decode("QYkqASAAIAAA")
    Match(cube_value=2, cube_holder=<Player.ZERO: 0>, player=<Player.ONE: 1>, crawford=False, game_state=<GameState.PLAYING: 1>, turn=<Player.ONE: 1>, double=False, resign=<Resign.NONE: 0>, dice=(5, 2), length=9, player_0_score=2, player_1_score=4)
    """
    match_bytes: bytes = base64.b64decode(match_id)
    match_key: str = "".join([format(b, "08b")[::-1] for b in match_bytes])
    return Match(
        cube_value=2 ** int(match_key[0:4][::-1], 2),
        cube_holder=Player(int(match_key[4:6][::-1], 2)),
        player=Player(int(match_key[6])),
        crawford=bool(int(match_key[7])),
        game_state=GameState(int(match_key[8:11][::-1], 2)),
        turn=Player(int(match_key[11])),
        double=bool(int(match_key[12])),
        resign=Resign(int(match_key[13:15][::-1], 2)),
        dice=(int(match_key[15:18][::-1], 2), int(match_key[18:21][::-1], 2)),
        length=int(match_key[21:36][::-1], 2),
        player_0_score=int(match_key[36:51][::-1], 2),
        player_1_score=int(match_key[51:66][::-1], 2),
    )
