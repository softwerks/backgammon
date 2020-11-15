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
from typing import List, Optional, Tuple, Set

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

    def generate_plays(self) -> None:
        """Return a set of positions for all legal plays."""

        def checker_on_point(position: position.Position, point: int) -> bool:
            """Return True if the player has one or more checkers on the point."""
            return position.board_points[point - 1] > 0

        def point_is_open(position: position.Position, destination: int) -> bool:
            """Return True if the opponent isn't blocking the point."""
            return position.board_points[destination - 1] > -2

        def player_home(position: position.Position) -> Tuple[int, ...]:
            """Returns a sequence of the player's checkers in their home board."""
            home_board: Tuple[int, ...] = position.board_points[:POINTS_PER_QUADRANT]
            return tuple(n if n > 0 else 0 for n in home_board)

        def can_move(
            position: position.Position, move_type: MoveState, point: int, pips: int
        ) -> Tuple[bool, Optional[int], Optional[int]]:
            """Determine if the checker can move the pips and return the source and destination points."""
            destination: int = point - pips
            if move_type is MoveState.BEAR_OFF:
                checkers_on_higher_points: int = sum(player_home(position)[point:])
                if destination < 1 and not checkers_on_higher_points:
                    return True, point, None
                elif point_is_open(position, destination):
                    return True, point, destination
            elif move_type is MoveState.ENTER_FROM_BAR:
                if point_is_open(position, pips):
                    return True, None, pips
            else:
                if destination > 0 and point_is_open(position, destination):
                    return True, point, destination
            return False, None, None

        def get_move_state(position: position.Position) -> MoveState:
            """Returns the type of move allowed."""
            if sum(player_home(position)) + position.player_off == CHECKERS:
                return MoveState.BEAR_OFF
            elif position.player_bar > 0:
                return MoveState.ENTER_FROM_BAR
            else:
                return MoveState.DEFAULT

        def generate_moves(pos: position.Position, dice: Tuple[int, ...]) -> None:
            """Generate all legal moves."""
            pips: int = dice[0]
            move_state: MoveState = get_move_state(pos)
            for point in range(POINTS, 0, -1):
                if checker_on_point(pos, point):
                    move_is_valid, source, destination = can_move(
                        pos, move_state, point, pips
                    )
                    if move_is_valid:
                        print(
                            f"{move_state} pips: {pips}, source: {source}, destination: {destination}"
                        )
                        next_position: position.Position = position.apply_move(
                            pos, source, destination
                        )
                        if len(dice) > 1:
                            generate_moves(next_position, dice[1:])

        doubles: bool = self.match.dice[0] == self.match.dice[1]
        dice: Tuple[int, ...] = self.match.dice * 2 if doubles else self.match.dice

        generate_moves(self.position, dice)
        if not doubles:
            generate_moves(self.position, tuple(reversed(dice)))

        # trim shorter plays

        # return plays

    def play(self, moves: List[Tuple[Optional[int], Optional[int]]]) -> None:
        """Excecute a play (i.e. a list of moves)."""
        new_position: position.Position = self.position
        for source, destination in moves:
            new_position = position.apply_move(new_position, source, destination)

        legal_positions: Set[position.Position] = set()

        if new_position in legal_positions:
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
