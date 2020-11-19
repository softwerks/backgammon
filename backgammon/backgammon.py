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
import operator
from typing import Callable, List, Optional, Tuple, Set

from backgammon import match
from backgammon import position

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


class Backgammon:
    def __init__(
        self, position_id: str = STARTING_POSITION_ID, match_id: str = STARTING_MATCH_ID
    ):
        self.position: position.Position = position.decode(position_id)
        self.match: match.Match = match.decode(match_id)

    def generate_plays(self) -> List[position.Play]:
        """Generate legal plays and return a set of the corresponding positions."""

        def get_player_home(pos: position.Position) -> Tuple[int, ...]:
            """Return a sequence of the player's checkers in their home board."""
            home_board: Tuple[int, ...] = pos.board_points[:POINTS_PER_QUADRANT]
            return tuple(point if point > 0 else 0 for point in home_board)

        def get_move_state(pos: position.Position) -> MoveState:
            """Return the move state, which determines the types of moves allowed."""
            move_state: MoveState = MoveState.DEFAULT
            if pos.player_bar > 0:
                move_state = MoveState.ENTER_FROM_BAR
            else:
                player_home: int = sum(get_player_home(pos))
                if player_home + pos.player_off == CHECKERS:
                    move_state = MoveState.BEAR_OFF
            return move_state

        def try_default(
            pos: position.Position, source: int, pips: int
        ) -> Optional[position.Move]:
            """Try to move a checker from one point to another and return the move if valid."""
            if pos.board_points[source - 1] > 0:
                destination: int = source - pips
                if destination > 0 and pos.board_points[destination - 1] > -2:
                    return position.Move(pips, source, destination)
            return None

        def try_enter_from_bar(
            pos: position.Position, pips: int
        ) -> Optional[position.Move]:
            """Try to move a checker from the bar to a point and return the move if valid."""
            destination: int = POINTS - (pips - 1)
            if pos.board_points[destination - 1] > -2:
                return position.Move(pips, None, destination)
            return None

        def try_bear_off(
            pos: position.Position, source: int, pips: int
        ) -> Optional[position.Move]:
            """Try to bear off a checker or move a checker from one point to another and return the move if valid."""
            if pos.board_points[source - 1] > 0:
                destination: int = source - pips
                if destination < 1:
                    higher_points: int = sum(get_player_home(pos)[:source])
                    if higher_points == 0:
                        return position.Move(pips, source, None)
                else:
                    return try_default(pos, source, pips)
            return None

        def generate(
            pos: position.Position,
            dice: Tuple[int, ...],
            moves: List[position.Move],
            plays: List[position.Play],
        ) -> List[position.Play]:
            """Generate legal plays."""
            if dice:
                pips: int = dice[0]

                move_state: MoveState = get_move_state(pos)

                move: Optional[position.Move] = None
                if move_state is MoveState.DEFAULT:
                    for source in range(POINTS, 0, -1):
                        move = try_default(pos, source, pips)
                        if move:
                            generate(
                                position.apply_move(pos, move),
                                dice[1:],
                                moves + [move],
                                plays,
                            )
                elif move_state is MoveState.ENTER_FROM_BAR:
                    move = try_enter_from_bar(pos, pips)
                    if move:
                        generate(
                            position.apply_move(pos, move),
                            dice[1:],
                            moves + [move],
                            plays,
                        )
                elif move_state is MoveState.BEAR_OFF:
                    for source in range(POINTS_PER_QUADRANT, 0, -1):
                        move = try_bear_off(pos, source, pips)
                        if move:
                            generate(
                                position.apply_move(pos, move),
                                dice[1:],
                                moves + [move],
                                plays,
                            )
            else:
                plays.append(position.Play(tuple(moves), pos))
            return plays

        def remove_smaller(plays: List[position.Play]) -> List[position.Play]:
            """Return a list of plays that use the maximum number of moves."""
            max_play: int = max(len(p.moves) for p in plays)
            if max_play == 1:
                return list(filter(lambda p: len(p.moves) == max_play, plays))
            return plays

        def remove_lower(
            plays: List[position.Play], dice: Tuple[int, ...]
        ) -> List[position.Play]:
            """Return a list of plays that most pips."""
            higher_die: int = max(dice)
            higher_plays: List[position.Play] = list(
                filter(lambda p: p.moves[0].pips == higher_die, plays)
            )
            return higher_plays if higher_plays else plays

        def remove_duplicate(plays: List[position.Play]) -> List[position.Play]:
            """Return a list of plays that result in unique board positions."""
            key_func: Callable = lambda p: hash(p.board)
            plays = sorted(plays, key=key_func)
            return list(
                map(
                    next,
                    map(operator.itemgetter(1), itertools.groupby(plays, key_func)),
                )
            )

        doubles: bool = self.match.dice[0] == self.match.dice[1]
        dice: Tuple[int, ...] = self.match.dice * 2 if doubles else self.match.dice

        plays: List[position.Play] = generate(self.position, dice, [], [])
        if not doubles:
            plays += generate(self.position, tuple(reversed(dice)), [], [])

        plays = remove_smaller(plays)
        if not doubles:
            plays = remove_lower(plays, dice)
        plays = remove_duplicate(plays)

        return plays

    def play(self, moves: Tuple[position.Move, ...]) -> None:
        """Excecute a play, a sequence of moves."""
        new_position: position.Position = self.position
        for move in moves:
            new_position = position.apply_move(new_position, move)

        legal_plays: List[position.Play] = self.generate_plays()

        if new_position in [play.board for play in legal_plays]:
            self.position = new_position
        else:
            position_id: str = position.encode(self.position)
            match_id: str = match.encode(self.match)
            raise BackgammonError(f"Invalid move: {position_id}:{match_id} {moves}")

    def __repr__(self):
        position_id: str = position.encode(self.position)
        match_id: str = match.encode(self.match)
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
            """Return a position split into top (match.Player.ZERO 12-1) and bottom (match.Player.ZERO 13-24) halves."""

            def normalize(position: List[int]) -> List[int]:
                """Return position for match.Player.ZERO"""
                if self.match.player is match.Player.ONE:
                    position = list(map(lambda n: -n, position[::-1]))
                return position

            position = normalize(position)

            half_len: int = int(len(position) / 2)
            top: List[int] = position[:half_len][::-1]
            bottom: List[int] = position[half_len:]

            return top, bottom

        points: List[List[str]] = checkers(*split(self.position.board_points))

        bar: List[List[str]] = checkers(
            *split([self.position.player_bar, self.position.opponent_bar,])
        )

        ascii_board: str = ""
        position_id: str = position.encode(self.position)
        ascii_board += f"                 Position ID: {position_id}\n"
        match_id: str = match.encode(self.match)
        ascii_board += f"                 Match ID   : {match_id}\n"
        ascii_board += (
            " "
            + (ASCII_12_01 if self.match.player is match.Player.ZERO else ASCII_13_24)
            + "\n"
        )
        for i in range(len(points)):
            ascii_board += (
                ("^|" if self.match.player == 0 else "v|")
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
            + (ASCII_13_24 if self.match.player is match.Player.ZERO else ASCII_12_01)
            + "\n"
        )

        return ascii_board
