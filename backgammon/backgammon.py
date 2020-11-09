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
from typing import List, Tuple

from backgammon import match
from backgammon.match import Match, Player
from backgammon import position
from backgammon.position import Position

STARTING_POSITION_ID = "4HPwATDgc/ABMA"
STARTING_MATCH_ID = "cAgAAAAAAAAA"

POINTS = 24
POINTS_PER_QUADRANT = int(POINTS / 4)

ASCII_BOARD_HEIGHT = 11
ASCII_MAX_CHECKERS = 5
ASCII_13_24 = "+13-14-15-16-17-18------19-20-21-22-23-24-+"
ASCII_12_01 = "+12-11-10--9--8--7-------6--5--4--3--2--1-+"


class Backgammon:
    def __init__(self, position_id: str = STARTING_POSITION_ID, match_id: str = STARTING_MATCH_ID):
        self.position: Position = position.decode(position_id)
        self.match: Match = match.decode(match_id)

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
                    self.position.opponent_bar,
                ]
            )
        )

        ascii_board: str = ""
        position_id: str = position.encode(self.position)
        ascii_board += f"                 Position ID: {position_id}\n"
        match_id: str = match.encode(self.match)
        ascii_board += f"                 Match ID   : {match_id}\n"
        ascii_board += (
            " " + (ASCII_12_01 if self.match.player is Player.ZERO else ASCII_13_24) + "\n"
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
            " " + (ASCII_13_24 if self.match.player is Player.ZERO else ASCII_12_01) + "\n"
        )

        return ascii_board
