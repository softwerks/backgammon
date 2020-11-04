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

from typing import List

import backgammon
from backgammon import position


class Board:
    def __init__(self, position_id: str = backgammon.STARTING_POSITION_ID):
        position_key = position.decode(position_id)
        self.position: List[List[int]] = position.position_from_key(position_key)
        self.dice_owner: int = 0

    def __str__(self):
        board: List[List[str]] = [["   " for j in range(12)] for i in range(11)]

        def checkers(
            board: List[List[str]], position: List[int], top: bool, checker: str
        ) -> List[List[str]]:
            for i, checkers in enumerate(position):
                row: int = 0 if top else 10
                while checkers > 0:
                    board[row][i] = checker
                    checkers -= 1
                    row += 1 if top else -1
            return board

        def p0_checkers(board: List[List[str]], position: List[int]) -> List[List[str]]:
            board = checkers(board, position[:12][::-1], True, " O ")
            board = checkers(board, position[12:24], False, " O ")
            return board

        def p1_checkers(board: List[List[str]], position: List[int]) -> List[List[str]]:
            board = checkers(board, position[12:24], True, " X ")
            board = checkers(board, position[:12][::-1], False, " X ")
            return board

        board = p0_checkers(board, self.position[0 if self.dice_owner is 0 else 1])
        board = p1_checkers(board, self.position[0 if self.dice_owner is 1 else 1])

        # bar pos[25]

        ascii_board: str = ""
        position_id: str = position.encode(position.key_from_position(self.position))
        ascii_board += f"Position ID: {position_id}\n"
        ascii_board += "+13-14-15-16-17-18-19-20-21-22-23-24-+\n"
        for i in range(len(board)):
            ascii_board += "|"
            ascii_board += "".join(board[i])
            ascii_board += "|"
            ascii_board += "\n"
        ascii_board += "+12-11-10--9--8--7--6--5--4--3--2--1-+\n"
        return ascii_board
