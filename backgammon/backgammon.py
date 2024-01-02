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

import enum
import itertools
import json
import operator
import random
from typing import Callable, List, NamedTuple, Optional, Tuple, Set

import backgammon.match
from backgammon.match import Player, GameState, Resign
import backgammon.position

MatchType = backgammon.match.Match
PositionType = backgammon.position.Position

STARTING_POSITION_ID = "4HPwATDgc/ABMA"
STARTING_MATCH_ID = "cAgAAAAAAAAA"

CHECKERS = 15
POINTS = 24
POINTS_PER_QUADRANT = int(POINTS / 4)

ASCII_BOARD_HEIGHT = 11
ASCII_MAX_CHECKERS = 5
ASCII_13_24 = "+13-14-15-16-17-18------19-20-21-22-23-24-+"
ASCII_12_01 = "+12-11-10--9--8--7-------6--5--4--3--2--1-+"


class BackgammonError(Exception):
    pass


class MoveState(enum.Enum):
    BEAR_OFF = enum.auto()
    ENTER_FROM_BAR = enum.auto()
    DEFAULT = enum.auto()


class Move(NamedTuple):
    pips: int
    source: Optional[int]
    destination: Optional[int]


class Play(NamedTuple):
    moves: Tuple[Move, ...]
    position: PositionType


class Backgammon:
    def __init__(
        self, position_id: str = STARTING_POSITION_ID, match_id: str = STARTING_MATCH_ID
    ):
        self.position: PositionType = backgammon.position.decode(position_id)
        self.match: MatchType = backgammon.match.decode(match_id)

    def generate_plays(self) -> List[Play]:
        """Generate and return legal plays."""

        def generate(
            position: PositionType,
            dice: Tuple[int, ...],
            die: int = 0,
            moves: Tuple[Move, ...] = (),
            plays: List[Play] = [],
        ) -> List[Play]:
            """Generate and return all plays."""
            new_position: Optional[PositionType]
            destination: Optional[int]
            point: int
            num_checkers: int
            pips: int

            if die < len(dice):
                pips = dice[die]

                if position.player_bar > 0:
                    new_position, destination = position.enter(pips)
                    if new_position:
                        generate(
                            new_position,
                            dice,
                            die + 1,
                            moves + (Move(pips, None, destination),),
                            plays,
                        )
                elif sum(position.player_home()) + position.player_off == CHECKERS:
                    for point, num_checkers in enumerate(
                        position.board_points[:POINTS_PER_QUADRANT]
                    ):
                        new_position, destination = position.off(point, pips)
                        if new_position:
                            generate(
                                new_position,
                                dice,
                                die + 1,
                                moves + (Move(pips, point, destination),),
                                plays,
                            )
                else:
                    for point, num_checkers in enumerate(position.board_points):
                        new_position, destination = position.move(point, pips)
                        if new_position:
                            generate(
                                new_position,
                                dice,
                                die + 1,
                                moves + (Move(pips, point, destination),),
                                plays,
                            )

            if len(moves) > 0:
                plays.append(Play(moves, position))

            return plays

        doubles: bool = self.match.dice[0] == self.match.dice[1]
        dice: Tuple[int, ...] = self.match.dice * 2 if doubles else self.match.dice

        plays: List[Play] = generate(self.position, dice)
        if not doubles:
            plays += generate(self.position, dice[::-1])

        if plays:
            max_moves: int = max(len(p.moves) for p in plays)
            if max_moves == 1:
                max_pips: int = max(dice)
                higher_plays: List[Play] = list(
                    filter(lambda p: p.moves[0].pips == max_pips, plays)
                )
                if higher_plays:
                    plays = higher_plays
            else:
                plays = list(filter(lambda p: len(p.moves) == max_moves, plays))

            key_func: Callable = lambda p: hash(p.position)
            plays = sorted(plays, key=key_func)
            plays = list(
                map(
                    next,
                    map(operator.itemgetter(1), itertools.groupby(plays, key_func)),
                )
            )

        return plays

    def start(self, length: int = 3) -> "Backgammon":
        self.match.game_state = GameState.PLAYING
        self.match.length = length
        self.first_roll()

        return self

    def roll(self) -> Tuple[int, int]:
        if self.match.dice != (0, 0):
            raise BackgammonError(f"Dice have already been rolled: {self.match.dice}")

        self.match.dice = (
            random.SystemRandom().randrange(1, 7),
            random.SystemRandom().randrange(1, 7),
        )
        return self.match.dice

    def first_roll(self) -> Tuple[int, int]:
        while True:
            self.match.dice = (
                random.SystemRandom().randrange(1, 7),
                random.SystemRandom().randrange(1, 7),
            )
            if self.match.dice[0] != self.match.dice[1]:
                break
        if self.match.dice[0] > self.match.dice[1]:
            self.match.player = Player.ZERO
            self.match.turn = Player.ZERO
        else:
            self.match.player = Player.ONE
            self.match.turn = Player.ONE
        return self.match.dice

    def play(
        self, moves: Tuple[Tuple[Optional[int], Optional[int]], ...]
    ) -> "Backgammon":
        """Excecute a play, a sequence of moves."""
        new_position: PositionType = self.position
        for source, destination in moves:
            new_position = new_position.apply_move(source, destination)

        legal_plays: List[Play] = self.generate_plays()

        if new_position in [play.position for play in legal_plays]:
            self.position = new_position

            if self.position.player_off == CHECKERS:
                multiplier: int = 1
                if self.position.opponent_off == 0:
                    if (
                        self.position.opponent_bar > 0
                        or sum(self.position.board_points[:POINTS_PER_QUADRANT]) != 0
                    ):
                        multiplier = 3
                    else:
                        multiplier = 2
                self.end_game(multiplier)
            else:
                self.end_turn()

        else:
            position_id: str = self.position.encode()
            match_id: str = self.match.encode()
            raise BackgammonError(f"Invalid move: {position_id}:{match_id} {moves}")

        return self

    def double(self) -> "Backgammon":
        if self.match.dice != (0, 0):
            raise BackgammonError("Cannot double: dice have been rolled")
        elif (
            self.match.cube_holder is not Player.CENTERED
            and self.match.cube_holder is not self.match.player
        ):
            raise BackgammonError("Cannot double: not cube holder")
        elif self.match.double:
            raise BackgammonError("Cannot double: already doubled")
        elif (
            self.match.player_0_score
            if self.match.player is Player.ZERO
            else self.match.player_1_score
        ) + self.match.cube_value >= self.match.length:
            raise BackgammonError("Cannot double: dead cube")
        elif self.match.crawford:
            raise BackgammonError("Cannot double: crawford game")

        self.match.double = True
        self.match.swap_turn()

        return self

    def accept_double(self) -> "Backgammon":
        if self.match.double:
            self.match.double = False
            self.match.cube_value *= 2
            self.match.cube_holder = (
                Player.ZERO if self.match.turn is Player.ZERO else Player.ONE
            )
            self.match.swap_turn()
        else:
            raise BackgammonError("Cannot accept double: double not offered")

        return self

    def reject_double(self) -> "Backgammon":
        if self.match.double:
            self.match.drop_cube()
            if self.match.game_state is GameState.PLAYING:
                self.match.reset_cube()
                self.position = backgammon.position.decode(STARTING_POSITION_ID)
                self.first_roll()
        else:
            raise BackgammonError("Cannot reject double: double not offered")

        return self

    def resign(self, resign_type: Resign) -> "Backgammon":
        if self.match.resign is Resign.NONE:
            self.match.resign = resign_type
            self.match.swap_turn()
        else:
            raise BackgammonError("Resignation has already been offered.")

        return self

    def accept_resignation(self) -> "Backgammon":
        if self.match.resign is not Resign.NONE:
            self.end_game(self.match.resign.value)
        else:
            raise BackgammonError("Resignation hasn't been offered")

        return self

    def reject_resignation(self) -> "Backgammon":
        if self.match.resign is not Resign.NONE:
            self.match.resign = Resign.NONE
            self.match.swap_turn()
        else:
            raise BackgammonError("Resignation hasn't been offered")

        return self

    def skip(self) -> "Backgammon":
        num_plays: int = len(self.generate_plays())
        if num_plays == 0:
            self.end_turn()
        else:
            raise BackgammonError(f"Cannot skip turn: {num_plays} possible plays")

        return self

    def end_turn(self) -> "Backgammon":
        self.position = self.position.swap_players()
        self.match.swap_players()
        self.match.reset_dice()

        return self

    def end_game(self, multiplier: int) -> "Backgammon":
        self.match.update_score(multiplier)

        self.match.resign = Resign.NONE

        if self.match.game_state is GameState.PLAYING:
            self.match.reset_cube()
            self.position = backgammon.position.decode(STARTING_POSITION_ID)
            self.first_roll()

        return self

    def encode(self) -> str:
        return f"{self.position.encode()}:{self.match.encode()}"

    def __repr__(self):
        position_id: str = self.position.encode()
        match_id: str = self.match.encode()
        return f"{__name__}.{self.__class__.__name__}('{position_id}', '{match_id}')"

    def __str__(self):
        def checkers(top: List[int], bottom: List[int]) -> List[List[str]]:
            """Return an ASCII checker matrix."""
            ascii_checkers: List[List[str]] = [
                ["   " for j in range(len(top))] for i in range(ASCII_BOARD_HEIGHT)
            ]

            for half in (top, bottom):
                for col, num_checkers in enumerate(half):
                    row: int = 0 if half is top else len(ascii_checkers) - 1
                    for i in range(abs(num_checkers)):
                        if (
                            abs(num_checkers) > ASCII_MAX_CHECKERS
                            and i == ASCII_MAX_CHECKERS - 1
                        ):
                            ascii_checkers[row][col] = f" {abs(num_checkers)} "
                            break
                        ascii_checkers[row][col] = " O " if num_checkers > 0 else " X "
                        row += 1 if half is top else -1

            return ascii_checkers

        def split(position: List[int]) -> Tuple[List[int], List[int]]:
            """Return a position split into top (Player.ZERO 12-1) and bottom (Player.ZERO 13-24) halves."""

            def normalize(position: List[int]) -> List[int]:
                """Return position for Player.ZERO"""
                if self.match.player is Player.ONE:
                    position = list(map(lambda n: -n, position[::-1]))
                return position

            position = normalize(position)

            half_len: int = int(len(position) / 2)
            top: List[int] = position[:half_len][::-1]
            bottom: List[int] = position[half_len:]

            return top, bottom

        points: List[List[str]] = checkers(*split(self.position.board_points))

        bar: List[List[str]] = checkers(
            *split(
                [
                    self.position.player_bar,
                    -self.position.opponent_bar,
                ]
            )
        )

        ascii_board: str = ""
        position_id: str = self.position.encode()
        ascii_board += f"                 Position ID: {position_id}\n"
        match_id: str = self.match.encode()
        ascii_board += f"                 Match ID   : {match_id}\n"
        ascii_board += (
            " "
            + (ASCII_12_01 if self.match.player is Player.ZERO else ASCII_13_24)
            + "\n"
        )
        for i in range(len(points)):
            ascii_board += (
                ("^|" if self.match.player is Player.ZERO else "v|")
                if i == int(ASCII_BOARD_HEIGHT / 2)
                else " |"
            )
            ascii_board += "".join(points[i][:POINTS_PER_QUADRANT])
            ascii_board += "|"
            ascii_board += "BAR" if i == int(ASCII_BOARD_HEIGHT / 2) else bar[i][0]
            ascii_board += "|"
            ascii_board += "".join(points[i][POINTS_PER_QUADRANT:])
            ascii_board += "|"
            ascii_board += "\n"
        ascii_board += (
            " "
            + (ASCII_13_24 if self.match.player is Player.ZERO else ASCII_12_01)
            + "\n"
        )

        return ascii_board
