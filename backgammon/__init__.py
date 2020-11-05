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

from backgammon import position

STARTING_POSITION_ID = "4HPwATDgc/ABMA"


class Backgammon:
    def __init__(self, position_id: str = STARTING_POSITION_ID):
        position_key: str = position.decode(position_id)
        self.position: List[int] = position.position_from_key(position_key)
        self.dice_owner: int = 0

    def __str__(self):
        board: List[List[str]] = [["   " for j in range(12)] for i in range(11)]

        def checkers(board: List[List[str]]) -> List[List[str]]:
            points: List[int] = self.position[1:25]

            def invert(points: List[int]) -> List[int]:
                return list(map(lambda n: -n, points[::-1]))

            if self.dice_owner == 0:
                points = invert(points)

            top: List[int] = points[12:]
            bottom: List[int] = points[:12][::-1]

            for half in (top, bottom):
                for i, checkers in enumerate(half):
                    row: int = 0 if half is top else 10
                    ascii_checker: str = " X " if checkers > 0 else " O "
                    count: int = 0
                    while count < abs(checkers):
                        if checkers > 5 and count == 4:
                            board[row][i] = f" {checkers} "
                            break
                        else:
                            board[row][i] = ascii_checker
                            count += 1
                            row += 1 if half is top else -1

            return board

        board = checkers(board)

        # bar pos[25]

        ascii_board: str = ""
        position_id: str = position.encode(position.key_from_position(self.position))
        ascii_board += f"Position ID: {position_id}\n"
        ascii_board += " +13-14-15-16-17-18-19-20-21-22-23-24-+\n"
        for i in range(len(board)):
            ascii_board += ("^|" if self.dice_owner == 0 else "v|") if i == 6 else " |"
            ascii_board += "".join(board[i])
            ascii_board += "|"
            ascii_board += "\n"
        ascii_board += " +12-11-10--9--8--7--6--5--4--3--2--1-+\n"
        return ascii_board
